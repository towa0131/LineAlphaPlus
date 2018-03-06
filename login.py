# -*- coding: utf-8 -*-

import LineAlpha
from LineAlpha.Api import LineClient
from LineAlpha.Api import LineTracer
from LineAPI.main import qr
import sys

client = LineClient.LineClient()

try:
	client.login(token=qr().get())
except:
	print ">> Login failed."
	sys.exit()

profile = client.getProfile()
setting = client.getSettings()
tracer = LineTracer.LineTracer(client)

print ">> Login successfully."
print ">> UserName : " + profile.displayName
print ">> MID : " + profile.mid
print ">> StatusMessage : " + profile.statusMessage

def RECEIVE_MESSAGE(op):
	message = op.message
	print message

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

while True:
	tracer.execute()
