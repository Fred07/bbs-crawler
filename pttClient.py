#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
import sys
import getpass
import time
import telnetlib
import keyAction as key

class pttClient:
	host = None
	account = None
	password = None
	removePrevConnect = False
	mode = None
	tn = None
	titleList = None
	errorMsg = None
	isConnect = False

	def __init__(self, host = None, account = None, pwd = None, removePrevConnect = True, mode = 'manuel'):
		self.host = host
		self.account = account
		self.password = pwd
		if (removePrevConnect):
			self.removePrevConnect = 'y'
		else:
			self.removePrevConnect = 'n'

		if (mode == 'config'):
			self.mode = 'config'
		else:
			self.mode = 'manuel'

	def isLogin(self):
		return self.isConnect

	def isConfigMode(self):
		if (self.mode == 'config'):
			return True

		return False

	def connect(self, host):
		try:
			self.host = host
			self.tn = telnetlib.Telnet(self.host)
			# self.tn.set_debuglevel(2)

			# Todo: 處理連線失敗的exception
			if (self.tn):
				self.setErrorMsg(u"已連線至 %s" % host)
				self.isConnect = True
				return True
			else:
				self.setErrorMsg(u"連線失敗，無法連線至 %s" % host)
				self.isConnect = False;
				return False
		except Exception:
			self.setErrorMsg(u"連線失敗，無法連線至 %s" % host)
			self.isConnect = False;
			return False

	def reConnect(self):
		print(u"重新連線中....")
		if (not self.host):
			self.setErrorMsg(u"連線失敗，無法連線至 %s" % self.host)
			return False

		if (not self.connect(self.host)):
			self.setErrorMsg(u"連線失敗，無法重新連線至 %s" % self.host)

	def login(self):
		print("開始進行登入...")
		content = self.tn.expect([u'或以 new 註冊:'.encode('big5')], 2)
		if (content[0] != -1):
			if (self.isConfigMode()):
				print("從config讀取登入資訊...")
				account = self.account
			else:
				account = raw_input("請輸入帳號: ")

			self.send(account, True)
			content = self.tn.expect([u'請輸入您的密碼:'.encode('big5')], 2)
			if (content[0] != -1):
				if (self.isConfigMode()):
					pwd = self.password
				else:
					pwd = getpass.getpass("請輸入密碼: ")

				self.send(pwd, True)
				content = self.tn.expect([u'您想刪除其他重複登入的連線嗎'.encode('big5')], 2)
				if (content[0] != -1):
					if (self.isConfigMode()):
						removePrevConnect = self.removePrevConnect
					else:
						removePrevConnect = raw_input("移除重複的連線? ")
					self.send(removePrevConnect, True)

				#等候進站畫面
				self.delay(1.5)

				#鍵盤'key down', 跳過進站畫面
				self.send(key.keyDown(), False)
				print("進入ptt了")

				content = self.tn.expect([u'您要刪除以上錯誤嘗試的記錄嗎?'.encode('big5')], 2)
				if (content[0] != -1):
					if (self.isConfigMode()):
						removeWrongAccess = 'y'
					else:
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
			self.send(key.keyDown(), False)

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
			command = key.keyLeft()
		if (command == 'right'):
			command = key.keyRight()
		if (command == 'up'):
			command = key.keyUp()
		if (command == 'down'):
			command = key.keyDown()
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
		keyWordList = re.findall(keyWord, content)
		# for m in keyWordList:
		# 	print "出現: " , keyWord

		print keyWord, "出現了", len(keyWordList), "次"

		return len(keyWordList)

	# Ctrl + l (重送畫面)
	def refresh(self):
		# self.send(u'\u000c', False, 0.5)
		self.send(key.keyRefresh(), False, 0.5)

	# 左轉, 右轉, End (目的為更新文章, 不適用search方式進入看板列表的情況)(該情況左轉會回到首頁控制板)
	def reload(self):
		# <--
		# self.send(u'\u001b[D', False, 1)
		self.send(key.keyLeft(), False, 1)

		# -->
		# self.send(u'\u001b[C', False, 1)
		self.send(key.keyRight(), False, 1)

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
