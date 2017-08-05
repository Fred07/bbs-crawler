#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import re
# import sys
import getpass
import time
import telnetlib
import keyaction as key


class PttClient:
    host = None
    account = None
    password = None
    removePrevConnect = False
    mode = None
    tn = None
    titleList = None
    errorMsg = None
    isConnect = False

    def __init__(self, host=None, account=None, pwd=None, remove_prev_connect=True, mode='manuel'):
        self.host = host
        self.account = account
        self.password = pwd
        if remove_prev_connect:
            self.removePrevConnect = 'y'
        else:
            self.removePrevConnect = 'n'

        if mode == 'config':
            self.mode = 'config'
        else:
            self.mode = 'manuel'

    def is_login(self):
        return self.isConnect

    def is_config_mode(self):
        if self.mode == 'config':
            return True

        return False

    def connect(self, host):
        try:
            self.host = host
            self.tn = telnetlib.Telnet(self.host)
            # self.tn.set_debuglevel(2)

            if self.tn:
                print(u"已連線至 %s" % host)
                self.isConnect = True
                return True
            else:
                self.set_error_msg(u"連線失敗，無法連線至 %s" % host)
                self.isConnect = False
                raise IOError
        except IOError:
            self.set_error_msg(u"連線失敗，無法連線至 %s" % host)
            self.isConnect = False
            return False

    def reconnect(self):
        print(u"重新連線中....")
        if not self.host:
            self.set_error_msg(u"連線失敗，無法連線至 %s" % self.host)
            return False

        if not self.connect(self.host):
            self.set_error_msg(u"連線失敗，無法重新連線至 %s" % self.host)

    def login(self):
        print("開始進行登入...")
        content = self.tn.expect([u'或以 new 註冊:'.encode('big5')], 2)
        if content[0] != -1:
            if self.is_config_mode():
                print("從config讀取登入資訊...")
                account = self.account
            else:
                account = input("請輸入帳號: ")

            self.send(account, True)
            content = self.tn.expect([u'請輸入您的密碼:'.encode('big5')], 2)
            if content[0] != -1:
                if self.is_config_mode():
                    pwd = self.password
                else:
                    pwd = getpass.getpass("請輸入密碼: ")

                self.send(pwd, True)
                content = self.tn.expect([u'您想刪除其他重複登入的連線嗎'.encode('big5')], 2)
                if content[0] != -1:
                    if self.is_config_mode():
                        remove_prev_connect = self.removePrevConnect
                    else:
                        remove_prev_connect = input("移除重複的連線? ")
                    self.send(remove_prev_connect, True)

                # 等候進站畫面
                self.delay(1.5)

                # 鍵盤'key down', 跳過進站畫面
                self.send(key.key_down(), False)
                print("進入ptt了")

                content = self.tn.expect([u'您要刪除以上錯誤嘗試的記錄嗎?'.encode('big5')], 2)
                if content[0] != -1:
                    if self.is_config_mode():
                        remove_wrong_access = 'y'
                    else:
                        remove_wrong_access = input("刪除錯誤嘗試紀錄? ")
                    self.send(remove_wrong_access, True)

        return True

    def go_to_board(self, name):

        # 's', 搜尋看板名稱
        self.send("s", False)
        content = self.tn.expect([u'請輸入看板名稱'.encode('big5')], 3)
        if content[0] != -1:
            # 進入指定看板
            self.send(name, True)

            print("進入" + name + "看板")

            # 跳過進版畫面
            self.send(key.key_down(), False)

            # read, (清空buffer)
            self.tn.read_very_eager()
            return True
        else:
            return False

    def control(self):
        self.refresh()
        command = input("下指令吧!!")

        # 特殊指令up,down,left,right
        if not command:
            command = u'\u000d'.encode('ascii', 'ignore')
        if command == 'left':
            command = key.key_left()
        if command == 'right':
            command = key.key_right()
        if command == 'up':
            command = key.key_up()
        if command == 'down':
            command = key.key_down()
        self.send(command, False)

        # show
        self.show_screen()

    def show_screen(self):
        content = self.tn.read_very_eager()
        print(content.decode('big5', 'ignore'))

    def detect_wording(self, key_word):
        self.refresh()
        content = self.tn.read_very_eager().decode('big5', 'ignore')
        key_word_list = re.findall(key_word, content)
        print("{:s}出現了{:d}次".format(key_word, len(key_word_list)))

        return len(key_word_list)

    # Ctrl + l (重送畫面)
    def refresh(self):
        self.send(key.key_refresh(), False, 0.5)

    # 左轉, 右轉, End (目的為更新文章, 不適用search方式進入看板列表的情況)(該情況左轉會回到首頁控制板)
    def reload(self):
        # <--
        self.send(key.key_left(), False, 1)

        # -->
        self.send(key.key_right(), False, 1)

        # End
        self.send(key.key_end(), False, 1)

    # send command
    def send(self, command, crlf=True, delay_time=0.5):
        if crlf:
            self.tn.write(command.encode('ascii', 'ignore') + b'\r\n')
        else:
            self.tn.write(command.encode('ascii', 'ignore'))

        self.delay(delay_time)

    @staticmethod
    def delay(delay_seconds):
        time.sleep(delay_seconds)

    def set_error_msg(self, error_msg):
        self.errorMsg = error_msg

    def get_error_msg(self):
        return self.errorMsg
