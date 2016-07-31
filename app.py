#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import time
import telnetlib

# print "%s" % (content,)
# sys.exit()

class pttClient:
	host = "ptt.cc"
	tn = None
	titleList = None

	def __init__(self):
		pass

	def login(self):
		host = self.host
		self.tn = telnetlib.Telnet(self.host)
		self.tn.set_debuglevel(2)
		print u"connect to %s" % host
		content = self.tn.expect([u'或以 new 註冊:'.encode('big5')], 3)
		if (content[0] != -1):
			account = raw_input("請輸入帳號: ")
			self.tn.write(account+'\r\n')
			print u"---step1---"
			content = self.tn.expect([u'請輸入您的密碼:'.encode('big5')], 3)
			if (content[0] != -1):
				pwd = raw_input("請輸入密碼: ")
				self.tn.write(pwd+'\r\n')
				print u"---step2---"
				content = self.tn.expect([u'您想刪除其他重複登入的連線嗎'.encode('big5')], 3)
				if (content[0] != -1):
					removePrevConnect = raw_input("移除重複的連線? ")
					self.tn.write(removePrevConnect+'\r\n')
					print u"---step3---"
					# self.tn.write("\u001b[B")

				else:
					# self.tn.write("\u001b[B")
					pass
			else:
				print "step2 failed"
		else:
			print "step1 failed"

		return True

	def getBoard(self):
		time.sleep(6)
		# self.tn.write("\u001b[B\r\n".encode('ascii', 'ignore'))
		# self.tn.write("[B".encode('ascii', 'ignore'))
		command = raw_input("do something!")
		self.tn.write(command + '\r\n')
		# self.tn.write("s\r\n")
		content = self.tn.expect([u'請輸入看板名稱'.encode('big5')], 3)
		if (content[0] != -1):
			print "yes!!!!"
		else:
			print "no!!!!"
		# sleep(2)
		# tn.write("")

pttClient = pttClient()
pttClient.login()
pttClient.getBoard()
