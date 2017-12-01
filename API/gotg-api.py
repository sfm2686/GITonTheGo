import os
import socket
import clamd
import uuid
from flask import Flask, request, redirect, url_for
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

