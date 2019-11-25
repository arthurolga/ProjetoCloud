#!/usr/local/bin/python3

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
from bson.objectid import ObjectId
from flask_pymongo import PyMongo
import requests
import json
import datetime
import os

from flask import Flask, redirect


app = Flask(__name__)
new_url = 'http://arthur-load-balancer-1469718616.us-east-1.elb.amazonaws.com:5000/todo/api/v1.0/'
username = "arthur"
password = "olga"


@app.route('/')
def root():
    print(new_url)
    return redirect(new_url, code=302)


@app.route('/<path:page>')
def anypage(page):
    return redirect('{new_url}/{page}'.format(page=page, new_url=new_url),
                    code=302)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
