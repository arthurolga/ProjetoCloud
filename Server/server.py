#!/usr/local/bin/python3

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import json
import datetime
import os

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()
app.config['MONGO_URI'] = os.environ['DB']
mongo = PyMongo(app)


@auth.get_password
def get_password(username):
    if username == 'arthur':
        return 'olga'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}


def make_json(dic):
    task = {
        '_id': str(dic["_id"]),
        'title': dic['title'],
        'description': dic['description'],
        'done': dic['done']
    }
    return task


class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True,
                                   help='No task title provided',
                                   location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        print(mongo)
        data = mongo.db.tasks.find()
        # [str(doc) for doc in data]  #
        return [make_json(doc) for doc in data]

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        # mongo.db.users.insert_one(data)
        mongo.db.tasks.insert_one(task)
        return {'message': 'ok!'}, 200


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        # task = [task for task in tasks if task['id'] == id]
        # if len(task) == 0:
        #     abort(404)
        # return {'task': marshal(task[0], task_fields)}
        data = mongo.db.tasks.find_one(
            {"_id": ObjectId(id)})
        return make_json(data)

    def put(self, id):
        args = self.reqparse.parse_args()
        task = {
            'title': args['title'],
            'description': args['description'],
            'done': args['done']
        }

        data = mongo.db.tasks.update_one(
            {"_id": ObjectId(id)}, {"$set": task})
        return {"updated": True}

        # task = [task for task in tasks if task['id'] == id]
        # if len(task) == 0:
        #     abort(404)
        # task = task[0]
        # args = self.reqparse.parse_args()
        # for k, v in args.items():
        #     if v is not None:
        #         task[k] = v
        # return {'task': marshal(task, task_fields)}

    def delete(self, id):
        data = mongo.db.tasks.delete_one(
            {"_id": ObjectId(id)})
        return {'result': data.deleted_count == 1}


class HealthAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super(HealthAPI, self).__init__()

    def get(self):
        return {'healthcheck': "Server ok!"}


api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<id>', endpoint='task')
api.add_resource(HealthAPI, '/todo/api/v1.0/', endpoint='healtcheck')


if __name__ == '__main__':
    app.run(debug=True)
