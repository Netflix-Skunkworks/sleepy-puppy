from logging import Formatter
from logging.handlers import RotatingFileHandler
from flask import Flask, redirect, request, abort, send_from_directory
from flask.ext import login
from flask.ext.bcrypt import Bcrypt
from flask.ext.restful import Api
from flask.ext.admin import Admin
from flask.ext.mail import Mail
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import flask_wtf
import os

# Config and App setups
app = Flask(__name__, static_folder='static')
app.config.from_object('config-default')
app.config.update(dict(
    PREFERRED_URL_SCHEME='https'
))
app.debug = app.config.get('DEBUG')

# Log handler functionality
handler = RotatingFileHandler(app.config.get('LOG_FILE'), maxBytes=10000000, backupCount=100)
handler.setFormatter(
    Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    )
)
handler.setLevel(app.config.get('LOG_LEVEL'))
app.logger.addHandler(handler)


def ssl_required(fn):
    """
    SSL decorator
    """
    @wraps(fn)
    def decorated_view(*args, **kwargs):
        if app.config.get("SSL"):
            if request.is_secure:
                return fn(*args, **kwargs)
            else:
                return redirect(request.url.replace("http://", "https://"))

        return fn(*args, **kwargs)

    return decorated_view

# CSRF Protection
csrf_protect = flask_wtf.CsrfProtect(app)

# Initalize DB object
db = SQLAlchemy(app)

# Initalize Bcrypt object for password hashing
bcrypt = Bcrypt(app)

# Initalize flask mail object for email notifications
flask_mail = Mail(app)

# Decorator for Token Auth on API Requests
from sleepypuppy.admin.admin.models import Administrator


def require_appkey(view_function):
    """
    Decorator for api using token based authetication
    """
    @wraps(view_function)
    def decorated_function(*args, **kwargs):

        # If the user is attempting to get list of puppyscripts
        # return the puppyscripts without token auth
        if request.method == "GET" and request.path.split('/')[2] == 'puppyscript_loader':
                return view_function(*args, **kwargs)
        if request.headers.get('Token'):
            for keys in Administrator.query.all():
                if request.headers.get('Token') == keys.api_key:
                    return view_function(*args, **kwargs)
            abort(401)
        else:
            abort(401)
    return decorated_function

# Initalize the Flask API
flask_api = Api(app, decorators=[csrf_protect.exempt, require_appkey])


def init_login():
    """
    Initalize the Flask Login manager
    """
    login_manager = login.LoginManager()
    login_manager.init_app(app)
    login_manager.session_protection = "strong"

    # Create user loader function
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(Administrator).get(user_id)

# Create the Flask Admin object
from admin.admin.views import MyAdminIndexView, AdministratorView
flask_admin = Admin(app,
                    'Sleepy Puppy',
                    index_view=MyAdminIndexView(url='/'),
                    base_template='admin/base.html',
                    template_mode='bootstrap3')

# Intalize the login manager for sleepy puppy
init_login()

# Import the collector which is used to collect capture information
from collector import views

# Import the screenshot upload handler
from upload import upload  # noqa

# Initalize all Flask API views
from api.views import PuppyscriptAssociations, CaptureView, CaptureViewList, PuppyscriptView, PuppyscriptViewList, PayloadView, PayloadViewList, AccessLogView, AccessLogViewList, AssessmentView, AssessmentViewList, GenericCollectorView, GenericCollectorViewList, AssessmentPayloads  # noqa

flask_api.add_resource(AssessmentViewList, '/api/assessments')
flask_api.add_resource(AssessmentView, '/api/assessments/<int:id>')
flask_api.add_resource(CaptureViewList, '/api/captures')
flask_api.add_resource(CaptureView, '/api/captures/<int:id>')
flask_api.add_resource(PuppyscriptView, '/api/puppyscript/<int:id>')
flask_api.add_resource(PuppyscriptViewList, '/api/puppyscript')
flask_api.add_resource(PayloadViewList, '/api/payloads')
flask_api.add_resource(PayloadView, '/api/payloads/<int:id>')
flask_api.add_resource(AccessLogViewList, '/api/access_log')
flask_api.add_resource(AccessLogView, '/api/access_log/<int:id>')
flask_api.add_resource(GenericCollectorViewList, '/api/generic_collector')
flask_api.add_resource(GenericCollectorView, '/api/generic_collector/<int:id>')
flask_api.add_resource(PuppyscriptAssociations, '/api/puppyscript_loader/<int:id>')
flask_api.add_resource(AssessmentPayloads, '/api/assessment_payloads/<int:id>')

# Initalize all Flask Admin dashboard views
from admin.capture.views import CaptureView
from admin.access_log.views import AccessLogView
from admin.puppyscript.views import PuppyscriptView
from admin.payload.views import PayloadView
from admin.user.views import UserView
from admin.assessment.views import AssessmentView
from admin.collector.views import GenericCollectorView

# Import the API views
from admin import views  # noqa

# Configure mappers for db associations
from sqlalchemy.orm import configure_mappers
configure_mappers()

# # Add all Flask Admin routes
flask_admin.add_view(PuppyscriptView(db.session))
flask_admin.add_view(PayloadView(db.session))
flask_admin.add_view(CaptureView(db.session))
flask_admin.add_view(GenericCollectorView(db.session))
flask_admin.add_view(AccessLogView(db.session))
flask_admin.add_view(UserView(db.session))
flask_admin.add_view(AssessmentView(db.session))
flask_admin.add_view(AdministratorView(Administrator, db.session))


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST')
    return response


# # Route to serve static asset files via Flask
@app.route('/static/<filename>')
def send_js(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
