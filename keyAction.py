#!/usr/bin/env python
# -*- coding: utf-8 -*- 

def keyUp(ascii = True):
	key = u'\u001b[A'
	if (ascii):
		key = key.encode('ascii', 'ignore')

	return key

def keyDown(ascii = True):
	key = u'\u001b[B'
	if (ascii):
		key = key.encode('ascii', 'ignore')

	return key

def keyLeft(ascii = True):
	key = u'\u001b[D'
	if (ascii):
		key = key.encode('ascii', 'ignore')

	return key

def keyRight(ascii = True):
	key = u'\u001b[C'
	if (ascii):
		key = key.encode('ascii', 'ignore')

	return key