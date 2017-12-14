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