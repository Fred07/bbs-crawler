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

		# Get parameters from config.yaml
		host       = config['host_config']['host']
		account    = config['host_config']['account']
		password   = config['host_config']['password']
		delayTime  = config['crawler_config']['cool_down_time']
		removeCon  = config['crawler_config']['remove_prev_connect']
		searchWord = config['crawler_config']['search_word']
		mode       = config['develop_config']['login_mode']

	pttHandler = pttClient.pttClient(host = host,
									 account = account,
									 pwd = password,
									 removePrevConnect = removeCon,
									 mode = mode)

	if (not pttHandler.connect("ptt.cc")):
		print pttHandler.getErrorMsg()
		exit()

	# Get search word from input
	if (len(sys.argv) > 1 and sys.argv[1]):
		searchWord = sys.argv[1]

	pttHandler.login()
	while (pttHandler.isLogin()):
			# pttHandler.control()
			pttHandler.getBoard("Gossiping")
			keyWordCount = pttHandler.detectWording(searchWord)
			if (keyWordCount >= 0):
				print('警告!!!{:s}出現超過{:s}次!!'.format(searchWord, keyWordCount))

			print('冷卻開始...%d秒' % delayTime)
			pttHandler.delay(delayTime)
			print('冷卻結束')
