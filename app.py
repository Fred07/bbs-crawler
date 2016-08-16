#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pttClient

pttClient = pttClient.pttClient()
pttClient.login()
if (pttClient.getBoard("Gossiping")):
	while (True):
		# pttClient.control()
		searchWord = '地震'
		keyWordCount = pttClient.detectWording(searchWord)

		if (keyWordCount > 10):
			print "警告!!!", searchWord, "出現超過", keyWordCount, "次!!"
		pttClient.getBoard("Gossiping")
		print '冷卻開始'
		pttClient.delay(30)
		print '冷卻結束'
else:
	print "進入看板失敗"