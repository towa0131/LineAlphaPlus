# -*- coding: utf-8 -*-

import LineAlpha
from LineAlpha.Api import LineClient
from LineAlpha.Api import LineTracer
from LineAPI.main import qr
import os
import sys
import datetime

client = LineClient.LineClient()

try:
	if os.path.exists("token.txt"):
		tokenFile = open("token.txt", "r")
		for tokenData in tokenFile:
			token = tokenData.strip()	
		tokenFile.close()
		client.login(token=token)
	else:
		token = qr().get()
		client.login(token=token)
		tokenFile = open("token.txt", "a")
		tokenFile.write(token)
		tokenFile.close()
except:
	print ">> Login failed."
	os.remove("token.txt")
	sys.exit()

profile = client.getProfile()
setting = client.getSettings()
tracer = LineTracer.LineTracer(client)

print ">> Login successfully."
print ">> UserName : " + profile.displayName
print ">> MID : " + profile.mid
print ">> StatusMessage : " + profile.statusMessage
print ">> Token : " + token

def NOTIFIED_INVITE_INTO_GROUP(op):
	gid = op.param1
	mid = op.param2
	try:
		user = client.findAndAddContactsByMid(mid)
		sendMessage("Invited group from " + user[mid].displayName, 13, 0)
	except:
		sendMessage("Invited group from Unknown", 13, 0)
	client.acceptGroupInvitation(gid)

tracer.addOpInterrupt(13, NOTIFIED_INVITE_INTO_GROUP)

def RECEIVE_MESSAGE(op):
	try:
		message = op.message
		sender = client.getContact(message.from_)
		msg = message.text
		name = sender.displayName
		mid = sender.mid
		pic = "http://dl.profile.line.naver.jp/" + sender.pictureStatus
		status = sender.statusMessage
		type = message.toType
		sendMessage("[" + name + "] " + msg, 26, 0)
	except Exception as e:
		pass

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

def sendMessage(message, opType, type = 0):
	if type == 0:
		prefix = "Info"
	elif type == 1:
		prefix = "Warning"
	elif type == 2:
		prefix = "Notice"
	elif type == 3:
		prefix = "Error"
	elif type == 4:
		prefix = "Debug"

	date = datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
	print date + " | " + prefix + " | " + str(opType) + " > " + message

while True:
	tracer.execute()
