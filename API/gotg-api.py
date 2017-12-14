import os
import socket
import clamd
import uuid
from flask import Flask, request, redirect, url_for
from redis import Redis, RedisError
from werkzeug.utils import secure_filename
from urlparse import urlparse


###########################################
## Global components and varibales
###########################################
VERSION = '/api/v1'
GIT_HUB = 'https://api.github.com'
REPO = 'OpenNl2' #TODO - REMOVE?
OWNER = 'rjswitzer3'
TOKEN = 'iuwevbuiwenviuoqwrnqviuowqr831093289328932'
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
# [POST] Initialize pull repo
# @params - lanuage, framework, libraries
# @return - Success: Container Initialized -> True | Fail: Failrue -> False
@app.route(VERSION + '/init/repo', methods=['POST'])
def init_repo():
    return response('Success', 200, None,)
    #TODO
    # 1. Create Dockerfile + requirements.txt
    # 2. write to requirements.txt
    # 3. Download repo
    # 4. Init fake filesystem
    
	
# [POST] Git commit
# @params - the commit message
# @return - Success: 'Some  mesage' | Fail: 'Failed to commit'
@app.route(VERSION + '/git/repo/commit', methods=['POST'])
def commit_code():
    if request.args.get('message') == '':
        return response('Bad Request', 400, None, 'None commit message provided')
    else:
        #TODO: python url builder + correct git request
        url = GIT_HUB+'/repos/'+OWNER+'/'+REPO+'/git/commits/'+TOKEN
        if requests.post(url, jsonify(message)):
            return response('Success', 200, None, 'Successful commity with message = ' + message)
        else:
            return response('Internal Servver Error', 500, None, 'Failed to commit git repo')
