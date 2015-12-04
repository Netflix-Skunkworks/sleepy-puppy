#     Copyright 2015 Netflix, Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
import urllib
from flask import request
from flask import render_template, make_response
from flask_mail import Message
from sleepypuppy import app, db, flask_mail, csrf_protect
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.collector.models import GenericCollector
from sleepypuppy.admin.access_log.models import AccessLog
from sleepypuppy.admin.assessment.models import Assessment
from sleepypuppy.admin.user.models import User
from flask import Response
from urlparse import urlparse


@app.route('/x', methods=['GET'])
def x_collector(payload=1):
    """
    Determine the payload assocaited with the request.
    If accesslog is enabled for the payload, record the event
    and email users subscribed to the payload's assessment.
    """

    the_payload = Payload.query.filter_by(
        id=int(request.args.get('u', 1))).first()
    assessment_id = request.args.get('a', 1)

    # consider only looking up payload one time for performance
    the_assessment = Assessment.query.filter_by(
        id=int(assessment_id)).first()

    try:
        if the_assessment.access_log_enabled:
            referrer = request.headers.get("Referrer", None)
            user_agent = request.headers.get("User-Agent", None)
            ip_address = request.access_route[-1]
            client_info = AccessLog(
                the_payload.id, the_assessment.name, referrer, user_agent, ip_address)
            db.session.add(client_info)
            db.session.commit()
            email_subscription(the_payload.id, the_assessment, None, client_info, 'access_log')
    except Exception as err:
        app.logger.warn("assessment not found, can't check access log.")
        app.logger.warn(err)

    # Log for recording access log records
    if request.args.get('u', 1):
        return collector(request.args.get('u', 1))


@app.route('/loader.js', methods=['GET'])
def collector(payload=1):
    """
    Render Puppyscript payload with unique identifier and hosts for callback.
    Enforce snooze and run_once directives.
    """
    payload = request.args.get('u', 1)
    assessment = request.args.get('a', 1)
    try:
        the_assessment = Assessment.query.filter_by(id=int(assessment)).first()
        if the_assessment.snooze:
            return ''
        if the_assessment.run_once and Capture.query.filter_by(payload=int(payload), assessment=the_assessment.name).first():
            return ''
        if the_assessment.run_once and GenericCollector.query.filter_by(payload=int(payload), assessment=the_assessment.name).first():
            return ''
    except Exception as err:
        app.logger.warn(err)
    # Render the template and include payload, hostname, callback_protocol,
    # assessment.
    # If you need to expose additiional server side
    # information for your JavaScripts, do it here.
    try:
        headers = {'Content-Type': 'text/javascript'}
        return make_response(render_template(
            'loader.js',
            payload=payload,
            assessment=the_assessment.id,
            hostname=app.config['CALLBACK_HOSTNAME'],
            callback_protocol=app.config.get('CALLBACK_PROTOCOL', 'https')),
            200,
            headers
        )
    except:
        app.logger.warn("Assessment not found, defaulting to General.")
        # If the assessment doesn't exist, default to general
        headers = {'Content-Type': 'text/javascript'}
        return make_response(render_template(
            'loader.js',
            payload=payload,
            assessment=1,
            hostname=app.config['CALLBACK_HOSTNAME'],
            callback_protocol=app.config.get('CALLBACK_PROTOCOL', 'https')),
            200,
            headers
        )


def email_subscription(payload, the_assessment, url, client_info, model):
    """
    Email notifications for captures, generic collections, and access log
    """
    email_list = []
    notify_jobs = Payload.query.filter_by(id=payload).first()
    user_notify = User.query.all()
    for user in user_notify:
        user_subscriptions = []
        for assessment in user.assessments:
            user_subscriptions.append(assessment.id)
        if the_assessment.id in user_subscriptions:
            email_list.append(user.email)

    import cgi
    if model == "capture":
        subject = "[Sleepy Puppy] - Capture Recieved From: {}".format(
            cgi.escape(url, quote=True)
        )
        html = "<b>Associated Assessment: </b>{}<br/>".format(
            cgi.escape(the_assessment.name, quote=True)
        )
        html += "<b>URL: </b>{}<br/>".format(
            cgi.escape(url, quote=True)
        )
        html += "<b>Payload: </b>{}<br/>".format(
            cgi.escape(notify_jobs.payload, quote=True)
        )
        if notify_jobs.notes is not None:
            html += "<b>Notes: </b>{}<br/>".format(
                cgi.escape(notify_jobs.notes, quote=True)
            )

        html += "<b>Capture: </b>{}://{}/capture/?flt1_0={}&flt3_14={}".format(
            app.config.get('CALLBACK_PROTOCOL', 'https'),
            app.config.get('HOSTNAME', 'localhost'),
            payload, the_assessment.name)

    elif model == "access_log":
        subject = "[Sleepy Puppy] - Access Log Request Recieved For Assessment(s): {}".format(
            cgi.escape(the_assessment.name, quote=True)
        )
        html = "<b>Associated Assessment: </b>{}<br/>".format(
            cgi.escape(the_assessment.name, quote=True)
        )
        html += "<b>Referer: </b>{}<br/>".format(
            cgi.escape(client_info.referrer or "", quote=True)
        )
        html += "<b>User Agent: </b>{}<br/>".format(
            cgi.escape(client_info.user_agent or "", quote=True)
        )
        html += "<b>IP Address: </b>{}<br/>".format(
            cgi.escape(client_info.ip_address, quote=True)
        )

        html += "<b>AccessLog: </b>{}://{}/accesslog/?flt1_7={}&flt2_14={}".format(
            app.config.get('CALLBACK_PROTOCOL', 'https'),
            app.config.get('HOSTNAME', 'localhost'),
            payload, the_assessment.name)

    elif model == "generic_collector":
        subject = "[Sleepy Puppy] - Generic Collector Recieved From: {}".format(
            cgi.escape(client_info.url, quote=True)
        )
        html = "<b>Associated Assessment: </b>{}<br/>".format(
            cgi.escape(the_assessment.name, quote=True)
        )
        html += "<b>Puppyscript Name: </b>{}<br/>".format(
            cgi.escape(client_info.puppyscript_name or "", quote=True)
        )
        html += "<b>Url: </b>{}<br/>".format(
            cgi.escape(client_info.url or "", quote=True)
        )
        html += "<b>Referer: </b>{}<br/>".format(
            cgi.escape(client_info.referrer or "", quote=True)
        )

        html += "<b>Generic Collector: </b>{}://{}/genericcollector/?flt1_0={}&flt2_7={}".format(
            app.config.get('CALLBACK_PROTOCOL', 'https'),
            app.config.get('HOSTNAME', 'localhost'),
            payload,
            the_assessment.name)

    # If there are people to email, email them that a capture was recieved
    if email_list:
        if app.config["EMAILS_USE_SES"]:
            import boto.ses
            try:
                ses_region = app.config.get('SES_REGION', 'us-east-1')
                ses = boto.ses.connect_to_region(ses_region)
            except Exception, e:
                import traceback
                app.logger.debug(Exception)
                app.logger.debug(e)
                app.logger.warn(traceback.format_exc())
                return

            for email in email_list:
                try:
                    ses.send_email(
                        app.config['MAIL_SENDER'],
                        subject,
                        html,
                        email,
                        format="html"
                    )
                    app.logger.debug("Emailed {} - {} ".format(email, subject))
                except Exception, e:
                    m = "Failed to send failure message to {} from {} with subject: {}\n{} {}".format(
                        email,
                        app.config['MAIL_SENDER'],
                        subject,
                        Exception,
                        e
                    )
                    app.logger.debug(m)
        else:
            msg = Message(
                subject,
                sender=app.config['MAIL_SENDER'],
                recipients=email_list
            )
            msg.html = html
            try:
                flask_mail.send(msg)
            except Exception as err:
                app.logger.debug(Exception)
                app.logger.debug(err)


@csrf_protect.exempt
@app.route('/generic_callback', methods=['POST', 'GET'])
def get_generic_callback():
    """
    Method to handle generic callbacks from arbitrary puppyscripts.

    Expects
    Method:          POST
    Data:            payload, puppyscript_name, data
    Optional Data:   referrer, url
    """
    response = Response()

    if request.method == 'POST':
        try:
            app.logger.info("request.form.get('payload', 0): {}".format(
                request.form.get('payload', 0)))

            puppyscript_name = urllib.unquote(
                unicode(request.form.get('puppyscript_name', '')))

            # If they don't set a url or referrer, ignore it
            url = urllib.unquote(unicode(request.form.get('uri', '')))
            referrer = urllib.unquote(
                unicode(request.form.get('referrer', '')))

            try:
                if app.config.get('ALLOWED_DOMAINS'):
                    domain = urlparse(url).netloc.split(':')[0]
                    if domain not in app.config.get('ALLOWED_DOMAINS'):
                        app.logger.info(
                            "Ignoring Capture from unapproved domain: [{}]".format(domain))
                        return response
            except Exception as e:
                app.logger.warn("Exception in /generic_callback when parsing url {}\n\n{}".format(Exception, str(e)))  # noqa

            data = urllib.unquote(unicode(request.form.get('data', '')))

            payload = Payload.query.filter_by(
                id=int(request.form.get('payload', 0))).first()

            assessment = Assessment.query.filter_by(
                id=int(request.form.get('assessment', 0))).first()

            # If it's a rogue capture, log it anyway.
            if payload is None or assessment is None:
                client_info = GenericCollector(
                    0, 0, puppyscript_name, url, referrer, data)
            else:
                # Create the capture with associated assessment/payload
                client_info = GenericCollector(
                    payload.id, assessment.name, puppyscript_name, url, referrer, data)

            db.session.add(client_info)
            db.session.commit()
            # Email users subscribed to the Payload's Assessment
            email_subscription(
                payload.id, assessment, url, client_info, 'generic_collector')
        except Exception as e:
            app.logger.warn(
                "Exception in /generic_callback {}\n\n{}".format(Exception, str(e)))
            import traceback
            traceback.print_exc()

    return response


# Disable CSRF protection on callback posts
@csrf_protect.exempt
@app.route('/callbacks', methods=['POST', 'GET'])
def get_callbacks():
    """
    Method to handle Capture creation.

    The Default Puppyscript provides all the expected parameters
    for this endpoint.

    If you need to modify the default captures, provide the following:

    Method:   POST
    Data:     assessment(payload.id will work here), url, referrer, cookies, user_agent, payload,
              screenshot, dom
    """
    response = Response()

    app.logger.info("Inside /callbacks")

    if request.method == 'POST':
        try:
            app.logger.info("request.form.get('payload', 0): {}".format(
                request.form.get('payload', 0)))

            url = urllib.unquote(unicode(request.form.get('uri', '')))

            if app.config.get('ALLOWED_DOMAINS'):
                domain = urlparse(url).netloc.split(':')[0]
                if domain not in app.config.get('ALLOWED_DOMAINS'):
                    app.logger.info(
                        "Ignoring Capture from unapproved domain: [{}]".format(domain))
                    return response

            referrer = urllib.unquote(
                unicode(request.form.get('referrer', '')))
            cookies = urllib.unquote(unicode(request.form.get('cookies', '')))
            user_agent = urllib.unquote(
                unicode(request.form.get('user_agent', '')))
            payload = Payload.query.filter_by(
                id=int(request.form.get('payload', 0))).first()
            assessment = Assessment.query.filter_by(
                id=int(request.form.get('assessment', 0))).first()
            screenshot = unicode(request.form.get('screenshot', ''))
            dom = urllib.unquote(unicode(request.form.get('dom', '')))[:65535]
            # If it's a rogue capture, log it anyway.
            if payload is None or assessment is None:
                client_info = Capture("Not found",
                                      url,
                                      referrer,
                                      cookies,
                                      user_agent,
                                      0,
                                      screenshot,
                                      dom)
            else:
                # Create the capture with associated assessment/payload
                client_info = Capture(assessment.name,
                                      url,
                                      referrer,
                                      cookies,
                                      user_agent,
                                      payload.id,
                                      screenshot,
                                      dom)

            db.session.add(client_info)
            db.session.commit()
            # Email users subscribed to the Payload's Assessment
            email_subscription(
                payload.id, assessment, url, client_info, 'capture')
        except Exception as e:
            app.logger.warn(
                "Exception in /callbacks {}\n\n{}".format(Exception, str(e)))
            import traceback
            traceback.print_exc()

    return response
