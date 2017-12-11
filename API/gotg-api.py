import os
import socket
import clamd
import uuid
import logging
from flask import Flask, request, redirect, url_for, jsonify
from redis import Redis, RedisError
from werkzeug.utils import secure_filename


###########################################
## Global components and varibales
###########################################
VERSION = '/api/v1'
app = Flask(__name__)

###########################################
## Helper FXs
###########################################
#Create JSON response
def response(status,code,data,message):
  return jsonify(status=status,
                  status_code=code,
                  data=data,
                  message=message)

###########################################
## API Endpoints
###########################################
# [GET] Login 
# @params credentials
# @return - Succes: TBD || Fail: TBD
@app.route(VERSION + '/init/user', methods=['GET'])
def init_user():
	return response('Success', 200, None, 'Successful request for nothing!')

# [GET] Homepage
# @params json data
# @return - Succes: valid data || Fail: invalid data
@app.route(VERSION + '/init/dockerfile', methods=['POST'])
def init_dockerfile():
	# TODO - determine if clean enough for dockerfile
	
	# JSON object to be used for dockerfile
	data = request.json
	# Cleaning json object
	if data["language"] == "N/A":
		data["language"] = ""
	if data["version"] == "-":
		data["version"] = ""
	if data["framework"] == "-":
		data["framework"] = ""

	return response('Success', 200, None, 'Successful submission of data for dockerfile!')