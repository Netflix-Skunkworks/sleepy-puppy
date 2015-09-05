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
from flask.ext.restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError
from sleepypuppy import db, app
from sleepypuppy.admin.puppyscript.models import Puppyscript
from sleepypuppy.admin.payload.models import Payload
from sleepypuppy.admin.capture.models import Capture
from sleepypuppy.admin.assessment.models import Assessment
from sleepypuppy.admin.access_log.models import AccessLog
from sleepypuppy.admin.collector.models import GenericCollector

# Request parser for API calls to Payload model
parser_payload = reqparse.RequestParser()
parser_payload.add_argument('assessments',
                            type=list,
                            required=False,
                            location='json')
parser_payload.add_argument('payload',
                            type=str,
                            required=False,
                            help="Payload Cannot Be Blank",
                            location='json')
parser_payload.add_argument('notes',
                            type=str,
                            location='json')

# Request parser for API calls to Assessment model
parser_assessment = reqparse.RequestParser()
parser_assessment.add_argument('name',
                               type=str,
                               required=False,
                               help="Assessment Name Cannot Be Blank",
                               location='json')
parser_assessment.add_argument('access_log_enabled',
                               type=bool,
                               required=False,
                               location='json')
parser_assessment.add_argument('snooze',
                               type=bool,
                               required=False,
                               location='json')
parser_assessment.add_argument('run_once',
                               type=bool,
                               required=False,
                               location='json')

# Request parser for API calls to Puppyscript model
parser_puppyscript = reqparse.RequestParser()
parser_puppyscript.add_argument('name',
                                type=str,
                                required=True,
                                help="Name Cannot Be Blank",
                                location='json')
parser_puppyscript.add_argument('code',
                                type=str,
                                required=True,
                                help="Code Cannot Be Blank",
                                location='json')
parser_puppyscript.add_argument('notes',
                                type=str,
                                required=False,
                                location='json')

parser_helper = reqparse.RequestParser()
parser_helper.add_argument('a',
                           type=str,
                           required=False)


class AssessmentView(Resource):

    """
    API Provides CRUD operations for a specific Assessment based on id.

    Methods:
    GET
    PUT
    DELETE
    """

    def get(self, id):
        """
        Retrieve an assessment based on id.
        """
        e = Assessment.query.filter(Assessment.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def put(self, id):
        """
        Update an assessment based on id.
        """
        args = parser_assessment.parse_args()
        e = Assessment.query.filter(Assessment.id == id).first()
        if e is not None:
            e.name = args["name"]
            e.access_log_enabled = args["access_log_enabled"]
            e.snooze = args["snooze"]
            e.run_once = args["run_once"]
        else:
            return 'assessment not found!'
        try:
            db.session.commit()
        except IntegrityError, exc:
            app.logger.warn(exc.message)
            return {"error": exc.message}, 500

        return e.as_dict(), 201

    def delete(self, id):
        """
        Delete an assessment based on id.
        """
        e = Assessment.query.filter(Assessment.id == id).first()
        if e is not None:
            try:
                # Delete everything asssociated with Assessment
                Capture.query.filter_by(assessment=e.name).delete()
                AccessLog.query.filter_by(assessment=e.name).delete()
                GenericCollector.query.filter_by(assessment=e.name).delete()
                db.session.delete(e)
                db.session.commit()
            except IntegrityError, exc:
                app.logger.warn(exc.message)
                return {"error": exc.message}, 500
        else:
            return {}

        return e.as_dict(), 204


class AssessmentViewList(Resource):

    """
    API Provides CRUD operations for Assessments.

    Methods:
    GET
    POST
    """

    def get(self):
        results = []
        for row in Assessment.query.all():
            results.append(row.as_dict())
        return results

    def post(self):
        args = parser_assessment.parse_args()
        o = Assessment()
        o.name = args["name"]
        o.access_log_enabled = args["access_log_enabled"]
        o.snooze = args["snooze"]
        o.run_once = args["run_once"]

        try:
            db.session.add(o)
            db.session.commit()
        except IntegrityError, exc:
            app.logger.warn(exc.message)
            return {"error": exc.message}, 500

        return o.as_dict(), 201


class PayloadView(Resource):

    """
    API Provides CRUD operations for Payloads based on id.

    Methods:
    GET
    PUT
    DELETE
    """

    def get(self, id):
        e = Payload.query.filter(Payload.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return 'payload not found!'

    def put(self, id):
        args = parser_payload.parse_args()
        e = Payload.query.filter(Payload.id == id).first()
        if e is not None:
            e.notes = args["notes"]
            e.payload = args["payload"]
        else:
            return 'payload not found!'
        try:
            db.session.commit()
        except IntegrityError, exc:
            app.logger.warn(exc.message)
            return {"error": exc.message}, 500

        return e.as_dict(), 201

    def delete(self, id):
        e = Payload.query.filter(Payload.id == id).first()
        if e is not None:
            try:
                db.session.delete(e)
                db.session.commit()
            except IntegrityError, exc:
                app.logger.warn(exc.message)
                return {"error": exc.message}, 500
        else:
            return {}

        return e.as_dict(), 204


class PayloadViewList(Resource):

    """
    API Provides CRUD operations for Payloads.

    Methods:
    GET
    POST
    """

    def get(self):
        results = []
        for row in Payload.query.all():
            results.append(row.as_dict())
        return results

    def post(self):

        args = parser_payload.parse_args()
        o = Payload()

        o.payload = args["payload"]
        o.ordering = 1
        o.notes = args["notes"]

        try:
            db.session.add(o)
            db.session.commit()
        except IntegrityError, exc:
            app.logger.warn(exc.message)
            return {"error": exc.message}, 500

        return o.as_dict(), 201


class PuppyscriptAssociations(Resource):

    """
    API Provides GET operations for retriving Puppyscripts associated with payload

    Methods:
    GET
    """

    def get(self, id):
        args = parser_helper.parse_args()
        the_list = []
        the_assessment = args['a']
        the_payload = Payload.query.filter(Payload.id == id).first()
        try:
            if the_payload is not None:
                for the_puppyscript in the_payload.ordering.split(','):
                    the_list.append(Puppyscript.query.filter_by(
                        id=int(the_puppyscript)).first().as_dict(the_payload.id, the_assessment))

                return the_list
            else:
                return {}
        except:
            return {}


class AssessmentPayloads(Resource):

    """
    API Provides GET operation for retriving Payloads associated with an Assessment

    Methods:
    GET
    """

    def get(self, id):
        the_list = []
        assessment = Assessment.query.filter_by(id=id).first()
        payloads = Payload.query.all()

        try:
            if assessment is not None:
                for payload in payloads:
                    results = payload.payload.replace("$1",
                                                      "//{}/x?u={}&a={}".format(app.config['HOSTNAME'], str(payload.id), str(assessment.id)))
                    the_list.append(results)
                return the_list
            else:
                return {}
        except:
            return {}


class PuppyscriptView(Resource):

    """
    API Provides CRUD operations for Puppyscripts based on id.

    Methods:
    GET
    PUT
    DELETE
    """

    def get(self, id):
        e = Puppyscript.query.filter(Puppyscript.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def put(self, id):
        args = parser_puppyscript.parse_args()
        e = Puppyscript.query.filter(Puppyscript.id == id).first()
        if e is not None:

            e.name = args["name"]
            e.code = args["code"]
            e.notes = args["notes"]
        else:
            return {'puppyscript not found!'}
        try:
            db.session.commit()
        except IntegrityError, exc:
            app.logger.warn(exc.message)
            return {"error": exc.message}, 500

        return e.as_dict(), 201

    def delete(self, id):
        result = Puppyscript.query.filter(Puppyscript.id == id).first()
        if result is not None:
            try:
                payloads = Payload.query.all()
                for payload in payloads:
                    if payload.ordering is not None:
                        payload.ordering = payload.ordering.replace(
                            str(result.id) + ",", "")
                        payload.ordering = payload.ordering.replace(
                            "," + str(result.id), "")
                        payload.ordering = payload.ordering.replace(
                            str(result.id), "")
                        db.session.add(payload)
                        db.session.commit()
            except Exception as err:
                app.logger.warn(err)
            try:
                db.session.delete(result)
                db.session.commit()
            except IntegrityError, exc:
                app.logger.warn(exc.message)
                return {"error": exc.message}, 500
        else:
            return {}


class PuppyscriptViewList(Resource):

    """
    API Provides CRUD operations for Puppyscripts.

    Methods:
    GET
    POST
    """

    def get(self):
        results = []
        for row in Puppyscript.query.all():
            results.append(row.as_dict())
        return results

    def post(self):

        args = parser_puppyscript.parse_args()
        o = Puppyscript()
        o.name = args["name"]
        o.code = args["code"]
        o.notes = args["notes"]

        try:
            db.session.add(o)
            db.session.commit()
        except IntegrityError, exc:
            app.logger.warn(exc.message)
            return {"error": exc.message}, 500

        return o.as_dict(), 201


class CaptureView(Resource):

    """
    API Provides CRUD operations for Captures based on id.

    Methods:
    GET
    DELETE

    Captures should be immutable so no PUT operations are permitted.
    """

    def get(self, id):
        e = Capture.query.filter(Capture.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def delete(self, id):
        capture = Capture.query.filter(Capture.id == id).first()
        if capture is not None:
            try:
                os.remove("uploads/{}.png".format(capture.screenshot))
                os.remove("uploads/small_{}.png".format(capture.screenshot))
            except:
                pass
            try:
                db.session.delete(capture)
                db.session.commit()
            except IntegrityError, exc:
                app.logger.warn(exc.message)
                return {"error": exc.message}, 500
        else:
            return {}

        return capture.as_dict(), 204


class CaptureViewList(Resource):

    """
    API Provides CRUD operations for Captures.

    Methods:
    GET
    """

    def get(self):
        results = []
        for row in Capture.query.all():
            results.append(row.as_dict())
        return results


class GenericCollectorView(Resource):

    """
    API Provides CRUD operations for Captures based on id.

    Methods:
    GET
    DELETE

    Captures should be immutable so no PUT operations are permitted.
    """

    def get(self, id):
        e = GenericCollector.query.filter(GenericCollector.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def delete(self, id):
        capture = GenericCollector.query.filter(
            GenericCollector.id == id).first()
        if capture is not None:
            try:
                db.session.delete(capture)
                db.session.commit()
            except IntegrityError, exc:
                app.logger.warn(exc.message)
                return {"error": exc.message}, 500
        else:
            return {}

        return capture.as_dict(), 204


class GenericCollectorViewList(Resource):

    """
    API Provides CRUD operations for Captures.

    Methods:
    GET
    """

    def get(self):
        results = []
        for row in GenericCollector.query.all():
            results.append(row.as_dict())
        return results


class AccessLogView(Resource):

    """
    API Provides CRUD operations for AccessLog based on id.

    Methods:
    GET
    DELETE

    Captures should be immutable so no PUT operations are permitted.
    """

    def get(self, id):
        e = AccessLog.query.filter(AccessLog.id == id).first()
        if e is not None:
            return e.as_dict()
        else:
            return {}

    def delete(self, id):
        access_log = AccessLog.query.filter(AccessLog.id == id).first()
        if access_log is not None:
            try:
                db.session.delete(access_log)
                db.session.commit()
            except IntegrityError, exc:
                app.logger.warn(exc.message)
                return {"error": exc.message}, 500
        else:
            return {}

        return access_log.as_dict(), 204


class AccessLogViewList(Resource):

    """
    API Provides CRUD operations for Access Log.

    Methods:
    GET
    """

    def get(self):
        results = []
        for row in AccessLog.query.all():
            results.append(row.as_dict())
        return results
