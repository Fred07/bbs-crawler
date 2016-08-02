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
		# self.tn.set_debuglevel(2)
		print u"connect to %s" % host
		content = self.tn.expect([u'或以 new 註冊:'.encode('big5')], 3)
		if (content[0] != -1):
			account = raw_input("請輸入帳號: ")
			self.tn.write(account+'\r\n')
			content = self.tn.expect([u'請輸入您的密碼:'.encode('big5')], 3)
			if (content[0] != -1):
				pwd = raw_input("請輸入密碼: ")
				self.tn.write(pwd+'\r\n')
				content = self.tn.expect([u'您想刪除其他重複登入的連線嗎'.encode('big5')], 3)
				if (content[0] != -1):
					removePrevConnect = raw_input("移除重複的連線? ")
					self.tn.write(removePrevConnect+'\r\n')
					# self.tn.write("\u001b[B")

				else:
					# self.tn.write("\u001b[B")
					pass
			else:
				print "step2 failed"
		else:
			print "step1 failed"

		return True

	def getBoard(self, name):
		time.sleep(5)

		#按一下鍵盤'下'跳過進站畫面
		# self.tn.write("\u001b[B".encode('ascii', 'ignore'))
		self.tn.write("[B".encode('ascii', 'ignore'))
		print("進入ptt了")

		self.tn.write("s".encode('ascii', 'ignore'))
		content = self.tn.expect([u'請輸入看板名稱'.encode('big5')], 3)
		if (content[0] != -1):
			self.tn.write(name + '\r\n')
			print("進入" + name + "看板")
			# self.tn.write("\u001b[B".encode('ascii', 'ignore'))
			self.tn.write("[B".encode('ascii', 'ignore'))
			return True;
		else:
			return False

	def control(self):
		self.tn.write('^L'.encode('ascii', 'ignore'))
		command = raw_input("下指令吧!!")
		if (not command):
			command = '\r\n'
		self.tn.write(command)
		content = self.tn.read_very_eager()
		print content

pttClient = pttClient()
pttClient.login()
if (pttClient.getBoard("Gossiping")):
	while (True):
		pttClient.control()
else:
	print "進入看板失敗"