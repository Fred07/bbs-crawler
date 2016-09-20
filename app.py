#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pttClient
import socket
import sys
import os
import yaml

if __name__ == '__main__':

	with open(os.path.dirname(__file__) + 'config/config.yaml', 'r') as f:
		config = yaml.load(f)

		# Get parameters
		host       = config['host_config']['host']
		account    = config['host_config']['account']
		password   = config['host_config']['password']
		delayTime  = config['crawler_config']['cool_down_time']
		searchWord = '地震'

	pttHandler = pttClient.pttClient()

	if (not pttHandler.connect("ptt.cc")):
		print pttHandler.getErrorMsg()
		exit()

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
