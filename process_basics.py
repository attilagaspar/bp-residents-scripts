import codecs
# -*- coding:Utf-8 -*-
#coding: utf-8
import locale
import csv
import os
import sys
import re
from msvcrt import getch
import difflib
import signal
from math import floor
#from fuzzywuzzy import fuzz
import operator
import msvcrt
import json
import time

def input():
    try:
            print 'Override?'
            foo = raw_input()
            return foo
    except:
            # timeout
            return

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

_digits = re.compile('\d')
def contains_digits(d):
	return bool(_digits.search(d))


def strip_number(candidate):

	hasDigits=[contains_digits(xx) for xx in candidate.split(u" ")]
	stringToCheck=u""
	goodList=[]
	for xxx in range(len(hasDigits)):
		if hasDigits[xxx]==0:
			goodList=goodList+[candidate.split(u" ")[xxx]]
		if hasDigits==1:
			break

	#print hasDigits
	stringToCheck=u" ".join(goodList)
	return stringToCheck



def kill_accents(inString):

	retstring = []
	for char in list(inString):
		if char==u"á" or char==u"Á":
			retstring=retstring+["a"]
		elif char==u"ä" or char==u"Ä":
			retstring=retstring+["a"]
		elif char==u"é" or char==u"É":
			retstring=retstring+["e"]
		elif char==u"ó" or char==u"Ó":
			retstring=retstring+["o"]
		elif char==u"ö" or char==u"Ö":
			retstring=retstring+["o"]
		elif char==u"ő" or char==u"Ő":
			retstring=retstring+["o"]
		elif char==u"ü" or char==u"Ü":
			retstring=retstring+["u"]
		elif char==u"ű" or char==u"Ű":
			retstring=retstring+["u"]
		elif char==u"ú" or char==u"Ú":
			retstring=retstring+["u"]
		elif char==u"í" or char==u"Í":
			retstring=retstring+["i"]
		else:
			retstring=retstring+[char]
	
	return "".join(retstring).lower()




def hun_sort(str1,str2):

	hunalph=['a','á','b','c','cs','d','dz','dzs','e','é','f','g','gy','h','i','í','j','k','l','ly','m','n','o','ó', 'ö', 'ő','p','q','r','s','sz','t','ty','u','ú', 'ü', 'ű', 'v', 'w', 'x', 'y', 'z', 'zs' ]
	dbls=['dz','gy','ly']
	

def unikill(str1):

	str2=u""
	for ch in str1:
		try:
			ch2=ch.encode('utf-8')
			str2=str2+ch2
		except:
			pass
	return str2

def dupl_drop(list1):

	list2=[]

	for i in list1:
		if i not in list2:
			list2=list2+[i]

	return list2

def wait_command(timeout):
	startTime = time.time()
	inp = None

	print "Press a key to override"
	while True:
		if msvcrt.kbhit():
			inp = msvcrt.getch()
			break
		elif time.time() - startTime > timeout:
			break

	if inp:
		print inp, " selected..."
		return inp
	else:
		print "proceeding"
		return None

def repair(str1):

	rxp=re.compile(u"[A-Z][a-z]*")
	if rxp.match(str1):
		return str1



def japanize(str1):
	str2=unikill(kill_accents(str1))

	todel=["sch","th", "gh", "hr", "ndtn", "ch", "cs", "ts", "eo", "w", "zs", "sz", "hn", "cz", "tz", "ck"]
	toput=["s"	,"t" , "g" , "r" , "ntn" , "c" , "c" , "c", "o",   "v", "z" , "s",  "n",  "c",  "c",  "k"]

	todel2=["gy","ny","ty"]
	toput2=["g", "n", "t"]

	for a in range(len(todel)):
		while todel[a] in str2:
			
			str2=str2.replace(todel[a],toput[a])

	for a in range(len(todel2)):
		while todel2[a] in str2:
			
			if str2[str2.find(todel2[a])]==str2[-2]:
				break
			else:
				str2=str2.replace(todel2[a],toput2[a])

	prevstr=""
	str3=""
	
	for a in range(len(str2)):
		if a>0:
			prevstr=str2[a-1]
		if str2[a]!=prevstr:
			str3=str3+str2[a]
			
	#utolsobetus korrigalasok
	str4=""

	if len(str3)>1:
		if str3[-1]=="y":
			str4=str3[:-1]+"i"
		else:
			str4=str3
	if len(str3)>2:
		if str3[-1]=="v" and str3[-2]!="o":
			str4=str3[:-1]+"i"
		else:
			str4=str3

	#print str2, unikill(str1)

	return str4