from __future__ import division
import os
import re
import socket
import uuid
import logging
import json
import docker
from collections import Counter
from flask import Flask, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from urlparse import urlparse


###########################################
## Global components and varibales
###########################################
VERSION = '/api/v1'
GIT_HUB = 'https://api.github.com'
DOCKER_DIRECTORY = '/docker'
JS_DIRECTORY = '../UI/js'
CSS_DIRECTORY = '../UI/css'
UI_DIRECTORY = '../UI'
REPO = ''

app = Flask(__name__)
app.config['DOCKER_DIRECTORY'] = DOCKER_DIRECTORY
app.config['JS_DIRECTORY'] = JS_DIRECTORY
app.config['CSS_DIRECTORY'] = CSS_DIRECTORY
app.config['UI_DIRECTORY'] = UI_DIRECTORY

DOCKER_CLIENT = docker.from_env()


###########################################
## Helper FXs
###########################################
#Create JSON response
def response(status,code,data,message):
  return jsonify(status=status,
                status_code=code,
                data=data,
                message=message)

#Build requirements.txt file
def init_requirements(framework,libraries):
    f = open("docker/requirements.txt","w+")
    f.write(framework+"\r\n")
    for lib in libraries:
        f.write(lib+"\r\n")

#Build Dockerfile
def init_dockerfile(language,version,repo):
    f = open("docker/Dockerfile","w+")
    f.write("FROM "+language+":"+version+"\r\n") #runtime
    f.write("WORKDIR /docker\r\n") #TODO repo directory
    f.write("ADD requirements.txt /docker\r\n") #req
    f.write("RUN pip install -r requirements.txt\r\n") #pip
    f.write("ADD . /docker\r\n")
    f.write("EXPOSE 80\r\n")
    f.write("ENV NAME World\r\n")
    f.write("CMD [""python"", ""gotg-api.py""]\r\n")


###########################################
## API Endpoints
###########################################
# Pages
@app.route('/', methods=['GET'])
def home():
    return send_from_directory(app.config['UI_DIRECTORY'], 'homePage.html')

@app.route('/shellPage', methods=['GET'])
def shell():
    return send_from_directory(app.config['UI_DIRECTORY'], 'shellPage.html')

@app.route('/statsPage', methods=['GET'])
def stats():
    return send_from_directory(app.config['UI_DIRECTORY'], 'statsPage.html')

# Resources
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(app.config['JS_DIRECTORY'], path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory(app.config['CSS_DIRECTORY'], path)


# [POST] Initialize pull repo
# @params - lanuage, framework, libraries as json
# @return - Success: Container Initialized -> True | Fail: Failrue -> False
@app.route(VERSION + '/init', methods=['POST'])
def init_repo():
    # JSON object to be used for dockerfile
    data = request.json
    # Cleaning json object
    if data["language"] == "N/A":
        data["language"] = ""
    if data["version"] == "-":
        data["version"] = ""
    if data["framework"] == "-":
        data["framework"] = ""
    REPO = data["repoLink"]
     #Stubbed until git functionality is available
    init_requirements(data["framework"], data["libraries"])
    init_dockerfile(data["language"], data["version"], data["repoLink"])
    #Check the dockerfiles exist
    if os.path.isfile(os.path.join(app.config['DOCKER_DIRECTORY'], 'requirements.txt')) \
        and os.path.isfile(os.path.join(app.config['DOCKER_DIRECTORY', 'Dockerfile'])):
        return response('Success',200,None,'Project initialized')
    else: #When would this be hit?
        return response('Failure',500,None,'Docker files failed to be created')

    
# [GET] Build the project in the docker container
# @params - execute flag
# @return - Success: TBD || Fail: Build / execution errors
@app.route(VERSION + '/build', methods=['GET'])
def build_docker():
    if request.args.get('execute') == '':
        return response('Bad Request', 400, None, 'Execution specifier required')
    run = request.args.get('execute')
    if run:
        img = DOCKER_CLIENT.images.build(app.config["DOCKER_DIRECTORY"])
        DOCKER_CLIENT.containers.run(img)
        return response('Success', 200, None, 'Project built and ran successfully with 0 warnings and 0 errors')
    else:
        img = DOCKER_CLIENT.images.build()#app.config["DOCKER_DIRECTORY"])
        con = DOCKER_CLIENT.containers.create(img)
        return response('Success', 200, None, 'Project built successfully with 0 warnings and 0 errors')
    

# [GET] Pull the project repo
#(This functionality is currently unavailable)
# @params - the repo link, owner, etc
# @return - Success: <Success Message> || Fail: <Failure message>
@app.route(VERSION + '/git/repo/pull', methods=['GET'])
def git_pull():
    #TODO
    # 1. LOTS (need to determine course of action)
    return response('Success', 200, None, 'Repository successfully pulled.')

	
# [POST] Git commit
# (This functionality is unavailable due to lack of text editing capabilities)
# @params - the commit message
# @return - Success: <Success Message> || Fail: <Failure message>
@app.route(VERSION + '/git/repo/commit', methods=['POST'])
def git_commit():
    if request.args.get('message') == None:
        return response('Bad Request', 403, None, 'Aborting commit due to empty commit message.')
    else:
        message = request.args.get('message')
        #return response('Success', 200, None, '[Stub] Commit success: ' + message)
        return response('Success', 200, None, 'Sorry! [commit] functionality is unavailble at this time')


# [GET] Git push
# (This functionality is unavailable due to lack of text editing capabilities)
# @params - branch name
# @return - Success: <Success Message> || Fail: <Failure message>
@app.route(VERSION + '/git/repo/push', methods=['POST'])
def git_push():
    # Stubbed response
    #return response('Success', 200, None, '[Stub] Project successfully pushed')
    return response('Success', 200, None, 'Sorry! [push] functionality is unavailble at this time')
    

# [GET] Stats
# @return - Succes: valid data processed || Fail: invalid data processed
@app.route(VERSION + '/git/stats', methods=['GET'])
def git_stats():
	# Making a dict and storing the results in
	stats = {}
	stats["table0"] = parseGitLog("git-log.txt", 'Author', userPercentageParser)
	stats["table1"] = parseGitLog("git-log.txt", 'Date:   ', dayPercentageParser)
	stats["table2"] = parseGitLog("git-log.txt", 'Date:   ', timePercentageParser)
	stats["table3"] = commitWord()
	# Returning a response with the data as the body
	return response('Success', 200, stats, 'Successful stats processed')

###########################################
## STATS PROCESSING METHODS
###########################################

# This is a generic method to do the processing of the first three stats tables
# from the git log since they are all percentages
#
# file: the git-log file
# stringInLine: the string identifying the line to be parsed
# method: the method to parse the line, each table has a different one
def parseGitLog(file, stringInLine, method):
	file = open(file, "r")

	# Making an array to count all occurrences and counting them in the loop
	allCount = []

	for line in file:
		if stringInLine in line:
			allCount.append(method(line))

	# A dict to reduce all occurrences to one key
	reduceCount = {}

	for thing in allCount:
		if thing in reduceCount:
			reduceCount[thing] += 1
		else:
			reduceCount[thing] = 1

	# Doing the calculations to get the percentage based on the
	# total number
	result = {}
	for thing in dict(Counter(reduceCount).most_common(10)):
		result[thing.replace("<", "(").replace(">", ")")] = round(((reduceCount[thing]/len(allCount)) * 100), 2)

	# Closing the file and returning the results dict
	file.close()

	return result

# This method parses a line in the git log to the author name and email
def userPercentageParser(line):
	return line[8:]

# This method parses a line in the git log to the get the day of the commit
def dayPercentageParser(line):
	return line[8:11]

# This method parses a line in the git log to get the time
def timePercentageParser(line):
	return line[19:21].replace(":", "")

# This method gathers all of the commit messages and counts the top 10
# most common ones
def commitWord():
	file = open("git-log.txt", "r")

	# Making an array to store all single words in the git messages
	proc = False
	words = []

	for line in file:
		# Marking the start of processing to set it to true
		if line.startswith("Date:   "):
			proc = True
			continue
		# Marking the end of processing and setting it to false
		elif line.startswith("commit"):
			proc = False
			continue
		# Processing the data to get alpha strings only
		if proc:
			words.extend(re.split("[^a-zA-Z]", line))

	# Making a dict for each word and its occurrences and counting the words
	wordsDict = {}

	for word in words:
		if word == ' ' or word == '':
			continue
		if word in wordsDict:
			wordsDict[word] += 1
		else:
			wordsDict[word] = 1

	# Closing the file and returning the results
	file.close()

	return dict(Counter(wordsDict).most_common(10))
	
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

