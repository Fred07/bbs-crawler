#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pttClient

delayTime = 30;
pttHandler = pttClient.pttClient()

if (not pttHandler.connect("ptt.cc")):
	print pttHandler.getErrorMsg()
	exit()

#### Test reConnect function
# if (not pttHandler.reConnect()):
# 	print pttHandler.getErrorMsg()
# 	exit()

pttHandler.login()
if (pttHandler.getBoard("Gossiping")):
	while (True):
		# pttHandler.control()
		searchWord = '地震'
		keyWordCount = pttHandler.detectWording(searchWord)

		if (keyWordCount > 10):
			print "警告!!!", searchWord, "出現超過", keyWordCount, "次!!"
		pttHandler.getBoard("Gossiping")
		print '冷卻開始...'
		pttHandler.delay(delayTime)
		print '冷卻結束'
else:
	print "進入看板失敗"