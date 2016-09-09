#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pttClient
import socket
import sys

if __name__ == '__main__':
	delayTime = 30;
	searchWord = '地震'
	pttHandler = pttClient.pttClient()

	if (not pttHandler.connect("ptt.cc")):
		print pttHandler.getErrorMsg()
		exit()

	#### Test reConnect function
	# if (not pttHandler.reConnect()):
	# 	print pttHandler.getErrorMsg()
	# 	exit()

	if (len(sys.argv) > 1 and sys.argv[1]):
		searchWord = sys.argv[1]

	pttHandler.login()
	while (pttHandler.isLogin()):
			# pttHandler.control()
			pttHandler.getBoard("Gossiping")
			keyWordCount = pttHandler.detectWording(searchWord)
			if (keyWordCount > 10):
				print "警告!!!", searchWord, "出現超過", keyWordCount, "次!!"

			print '冷卻開始...'
			pttHandler.delay(delayTime)
			print '冷卻結束'
	# except BaseException:
	# 	print 'Base Exception!!'
	# 	print 
	# 	exit()
	# except Exception:
	# 	print 'Exception!!'
	# 	exit()