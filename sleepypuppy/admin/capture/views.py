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
import os
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.actions import action
from flask.ext import login
from flask_wtf import Form
from sleepypuppy import app, db
from models import Capture


class CaptureView(ModelView):
    """
    ModelView override of Flask Admin for Captures.
    """
    # CSRF protection
    form_base_class = Form

    # Check if user is autheticated
    def is_accessible(self):
        return login.current_user.is_authenticated()

    # Override displayed fields
    list_template = 'capture_list.html'

    # Restrict captures from being created or edited
    can_create = False
    can_edit = False

    # Column tweaks
    column_list = (
        'pub_date',
        'payload',
        'assessment',
        'url',
        'referrer',
        'cookies',
        'user_agent',
        'dom',
        'screenshot'
    )

    column_sortable_list = (
        'pub_date',
        'payload',
        'assessment',
        'url',
        'referrer',
        'user_agent'
    )

    hostname = app.config['HOSTNAME']

    # Make sure payload exists otherwise it's a zombie capture
    column_formatters = dict(
        payload=lambda v, c, m, p: str(m.payload)
        if m.payload is not None else "Payload Not Found"
    )
    form_excluded_columns = ('captures')

    # Allow columns to be searched/sorted
    column_filters = ('id', 'payload', 'assessment', 'url')

    def delete_from_s3(self, filename):
        if app.config.get('UPLOAD_SCREENSHOTS_TO_S3', False):
            try:
                import boto
                from boto.s3.key import Key
                conn = boto.connect_s3()
                b = conn.get_bucket(app.config['S3_BUCKET'])
                k = Key(b)
                k.key = '{}/{}'.format(
                    app.config.get('S3_FILES_PREFIX', 'sleepypuppy'),
                    filename
                )
                k.delete()
            except Exception as e:
                app.logger.warn(
                    "Exception {}/{} removing {}/{} from s3".format(
                        Exception,
                        e,
                        app.config.get('S3_FILES_PREFIX', 'sleepypuppy'),
                        filename
                    )
                )

    # Delete screenshots on mass delete
    def delete_screenshots(self, model):
        """
        Remove screenshot assocaited with Capture model
        """
        try:
            os.remove("uploads/{}.png".format(model.screenshot))
            os.remove("uploads/small_{}.png".format(model.screenshot))
        except:
            pass

        self.delete_from_s3("{}.png".format(model.screenshot))
        self.delete_from_s3("small_{}.png".format(model.screenshot))

    on_model_delete = delete_screenshots

    @action('delete', 'Delete', 'Are you sure you want to delete?')
    def action_delete(self, items):
        for record in items:
            try:
                filename = str(Capture.query.filter_by(id=record).first().screenshot)
                os.remove("uploads/{0}.png".format(filename))
                os.remove("uploads/small_{0}.png".format(filename))
            except:
                pass

            self.delete_from_s3("{}.png".format(filename))
            self.delete_from_s3("small_{}.png".format(filename))

            page = Capture.query.get(record)
            db.session.delete(page)
            db.session.commit()

    def __init__(self, session, **kwargs):
        # You can pass name and other parameters if you want to
        super(CaptureView, self).__init__(Capture, session, **kwargs)
