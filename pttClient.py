#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import sys
import getpass
import time
import telnetlib

class pttClient:
	host = None
	tn = None
	titleList = None
	errorMsg = None

	def __init__(self):
		pass

	def connect(self, host = "ptt.cc"):
		self.host = host
		self.tn = telnetlib.Telnet(self.host)
		# self.tn.set_debuglevel(2)

		# Todo: 處理連線失敗的exception
		if (self.tn):
			# print u"連線至 %s" % host
			self.setErrorMsg(u"連線至 %s" % host)
			return True
		else:
			# print u"連線失敗"
			self.setErrorMsg(u"連線失敗")
			return False

	def login(self):
		content = self.tn.expect([u'或以 new 註冊:'.encode('big5')], 2)
		if (content[0] != -1):
			account = raw_input("請輸入帳號: ")
			self.send(account, True)
			content = self.tn.expect([u'請輸入您的密碼:'.encode('big5')], 2)
			if (content[0] != -1):
				pwd = getpass.getpass("請輸入密碼: ")
				self.send(pwd, True)
				content = self.tn.expect([u'您想刪除其他重複登入的連線嗎'.encode('big5')], 2)
				if (content[0] != -1):
					removePrevConnect = raw_input("移除重複的連線? ")
					self.send(removePrevConnect, True)

				#等候進站畫面
				self.delay(1.5)

				#鍵盤'key down', 跳過進站畫面
				self.send(u"\u001b[B", False)
				print("進入ptt了")

				content = self.tn.expect([u'您要刪除以上錯誤嘗試的記錄嗎?'.encode('big5')], 2)
				if (content[0] != -1):
					removeWrongAccess = raw_input("刪除錯誤嘗試紀錄? ")
					self.send(removeWrongAccess, True)

		return True

	def getBoard(self, name):
		# 's', 搜尋看板名稱
		self.send("s", False)
		content = self.tn.expect([u'請輸入看板名稱'.encode('big5')], 3)
		if (content[0] != -1):
			# 進入指定看板
			self.send(name, True)

			print("進入" + name + "看板")

			# 跳過進版畫面
			self.send(u"\u001b[B", False)

			# read, (清空buffer)
			self.tn.read_very_eager()
			return True;
		else:
			return False

	def control(self):
		self.refresh()
		command = raw_input("下指令吧!!")

		#特殊指令up,down,left,right
		if (not command):
			command = u'\u000d'.encode('ascii', 'ignore')
		if (command == 'left'):
			command = u'\u001b[D'.encode('ascii', 'ignore')
		if (command == 'right'):
			command = u'\u001b[C'.encode('ascii', 'ignore')
		if (command == 'up'):
			command = u'\u001b[A'.encode('ascii', 'ignore')
		if (command == 'down'):
			command = u'\u001b[B'.encode('ascii', 'ignore')
		self.send(command, False)

		# show
		self.showScreen()

	def showScreen(self):
		content = self.tn.read_very_eager()
		print content.decode('big5', 'ignore')

	def detectWording(self, keyWord):
		self.refresh()
		content = self.tn.read_very_eager().decode('big5', 'ignore')

		keyWord = keyWord.decode('utf-8', 'ignore')
		# keyWordList = re.finditer(keyWord, content)
		keyWordList = re.findall(keyWord, content)
		for m in keyWordList:
			print "出現: " , keyWord

		print keyWord, "出現了", len(keyWordList), "次"

		return len(keyWordList)

	# Ctrl + l (重送畫面)
	def refresh(self):
		self.send(u'\u000c', False, 0.5)

	# 左轉, 右轉, End (目的為更新文章, 不適用search方式進入看板列表的情況)(該情況左轉會回到首頁控制板)
	def reload(self):
		# <--
		self.send(u'\u001b[D', False, 1)

		# -->
		self.send(u'\u001b[C', False, 1)

		# End
		self.send(u'\u001b[F', False, 1)


	# send command
	def send(self, command, crlf = True, delayTime = 0.5):
		if (crlf):
			self.tn.write(command.encode('ascii', 'ignore') + '\r\n')
		else:
			self.tn.write(command.encode('ascii', 'ignore'))
		
		self.delay(delayTime)

	def delay(self, delaySeconds):
		time.sleep(delaySeconds)

	def setErrorMsg(self, errorMsg):
		self.errorMsg = errorMsg

	def getErrorMsg(self):
		return self.errorMsg
