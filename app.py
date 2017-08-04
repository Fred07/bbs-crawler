#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pttclient
import sys
import os
import yaml

if __name__ == '__main__':

    with open(os.path.dirname(__file__) + 'config/config.yaml', 'r') as f:
        config = yaml.load(f)

        # Get parameters from config.yaml
        host = config['host_config']['host']
        account = config['host_config']['account']
        password = config['host_config']['password']
        delayTime = config['crawler_config']['cool_down_time']
        removeCon = config['crawler_config']['remove_prev_connect']
        searchWord = config['crawler_config']['search_word']
        board = config['crawler_config']['board_list']
        mode = config['develop_config']['login_mode']

    pttHandler = pttclient.PttClient(host=host,
                                     account=account,
                                     pwd=password,
                                     remove_prev_connect=removeCon,
                                     mode=mode)

    if not pttHandler.connect("ptt.cc"):
        print(pttHandler.get_error_msg())
        exit()

    # Get search word from input
    if len(sys.argv) > 1 and sys.argv[1]:
        searchWord = sys.argv[1]

    pttHandler.login()
    while pttHandler.is_login():
        # pttHandler.control()
        pttHandler.go_to_board(board)
        keyWordCount = pttHandler.detect_wording(searchWord)
        if keyWordCount >= 10:
            print('警告!!!{:s}出現超過{:d}次!!'.format(searchWord, keyWordCount))

        print('冷卻開始...%d秒' % delayTime)
        pttHandler.delay(delayTime)
        print('冷卻結束')
