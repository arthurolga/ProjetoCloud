#!/usr/local/bin/python3

"""Alternative version of the ToDo RESTful server implemented using the
Flask-RESTful extension."""

from flask import Flask, jsonify, abort, make_response, request
from flask_restful import Api, Resource, reqparse, fields, marshal
from flask_httpauth import HTTPBasicAuth
import requests
import json
import datetime
import os


app = Flask(__name__)
new_url = os.environ['NEW_URL']
username = "arthur"
password = "olga"


@app.route('/')
def root():
    print(new_url)
    return requests.get(url=new_url).content


@app.route('/<path:page>', methods=['GET'])
def getpage(page):
    to_url = '{new_url}/{page}'.format(page=page, new_url=new_url)
    # print(to_url)
    # return redirect(to_url,
    #                 code=307)
    # red=requests.get(url="http://{}:5000/api/v1/users".format(redIp))
    r = requests.get(url=to_url)
    return r.content


@app.route('/<path:page>', methods=['POST'])
def postpage(page):
    to_url = '{new_url}/{page}'.format(page=page, new_url=new_url)
    # print(to_url)
    # return redirect(to_url,
    #                 code=307)
    r = requests.post(url=to_url, json=request.get_json())
    return r.content


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
