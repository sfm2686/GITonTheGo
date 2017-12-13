from __future__ import division
import os
import re
import socket
# import clamd
import uuid
import logging
import json
from collections import Counter
from flask import Flask, request, redirect, url_for, jsonify
# from redis import Redis, RedisError
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

# [GET] Stats 
# @return - Succes: valid data processed || Fail: invalid data processed
@app.route(VERSION + '/git/stats', methods=['GET'])
def git_stats():
	stats = {}
	stats["table0"] = userPercentage()
	stats["table1"] = dayPercentage()
	stats["table2"] = timePercentage()
	stats["table3"] = commitWord()
	# TODO - most common commit word

	# return response('Success', 200, jsonify(stats), 'Successful stats processed')
	return jsonify(stats)

###########################################
## STATS PROCESSING METHODS
###########################################
def userPercentage():
	file = open("git-log2.txt", "r")

	authors = []

	for line in file:
		if 'Author' in line:
			authors.append(line[8:])

	authorsDict = {}

	for author in authors:
		if author in authorsDict:
			authorsDict[author] += 1
		else:
			authorsDict[author] = 1

	result = {}

	for author in dict(Counter(authorsDict).most_common(10)):
		result[author] = round(((authorsDict[author]/len(authors)) * 100), 2)

	app.logger.info(result)

	return result

def dayPercentage():
	file = open("git-log2.txt", "r")

	days = []

	for line in file:
		if 'Date:   ' in line:
			days.append(line[8:11])

	daysDict = {}

	for day in days:
		if day in daysDict:
			daysDict[day] += 1
		else:
			daysDict[day] = 1

	result = {}
	for day in daysDict:
		result[day] = round(((daysDict[day]/len(days)) * 100), 2)

	return result

def timePercentage():
	file = open("git-log.txt", "r")

	times = []

	for line in file:
		if 'Date:   ' in line:
			times.append(line[19:21].replace(":", ""))

	timesDict = {}

	for time in times:
		if time in timesDict:
			timesDict[time] += 1
		else:
			timesDict[time] = 1

	result = {}

	for time in dict(Counter(timesDict).most_common(10)):
		result[time] = round(((timesDict[time]/len(times)) * 100), 2)

	return result

def commitWord():
	file = open("git-log2.txt", "r")

	proc = False
	words = []

	for line in file:
		if line.startswith("Date:   "):
			proc = True
			continue
		elif line.startswith("commit"):
			proc = False
		if proc:
			words.extend(re.split("[^a-zA-Z]", line))

	while '' in words:
		words.remove('')

	wordsDict = {}

	for word in words:
		if word in wordsDict:
			wordsDict[word] += 1
		else:
			wordsDict[word] = 1

	result = {}

	for word in dict(Counter(wordsDict).most_common(10)):
		result[word] = round(((wordsDict[word]/len(words)) * 100), 2)

	return result