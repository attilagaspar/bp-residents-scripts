#coding: utf-8
import codecs
# -*- coding:Utf-8 -*-


import difflib
import locale
import csv
import os
import sys
import re
from msvcrt import getch
import difflib
import signal
from math import floor
from fuzzywuzzy import fuzz
import operator
import msvcrt
import json
import time
import collections


from process_basics import *

####################################################################
# THIS IS TO CLEAN LAST NAMES AND OBTAIN A LIST
####################################################################



#### ENNEK KELLENE MAJD KISZURNI A KAMU KARAKTEREKET, egyelore persze nem teszi, mert egy kocsog



#KETTOSHANGZOK

#MSGH KETTOZES

#DIFTONGUS


	#(csorgeo) eo o 
	#ie     -i
	#ei, ay a eu

#NEMA HANGOK

	#ndtn ntn (brandtner)
	#hr - r
	#th - t
	#gh    --- g

#SZOVEGI ELKURASOK

	#szo vegi -el -l
	#szo vegi ch  h


#Y

#y --- i kiveve ha ny, gy, ty

	#ch cs ts --- c
	#cz tz 

	#ck     k

	#w - v
	#z - s

	#massalhangzokettozes
	#chr cr kr


	#sch ss ---- s
	#szo vegi -j -i
	
	#ny  -  n
	#gy	 -  g
	#







inFileName="paired_test.txt"

inFile = codecs.open("paired_test.txt",'r', encoding='utf-8', errors='replace')
pina = codecs.open("pina.txt",'w', encoding='utf-8', errors='replace')

rawnames = []
prevname=""

lndict={}
lninvdict={}

for line in inFile:
	name=line.split(",")[1]
	nameels=name.split()
	rawnames=rawnames+[nameels[0]]

for i in range(len(rawnames)):
	if i>0:
		prevname=rawnames[i-1]
	thisname=rawnames[i]
	status="FAK"
	
	#if thisname==prevname or sorted([kill_accents(prevname),kill_accents(thisname)])==[kill_accents(prevname),kill_accents(thisname)]:
	try:
		if thisname==prevname or sorted([kill_accents(prevname)[0],kill_accents(thisname)[0]])==[kill_accents(prevname)[0],kill_accents(thisname)[0]]:		
			status="OK"
	except:
		status="xxx"

	jap=japanize(thisname)
	lc = kill_accents(thisname)
	if jap!=lc:
		if jap not in lndict:
			lndict[jap]=[lc]
		if jap in lndict:
			if lc not in lndict[jap]:
				lndict[jap]=lndict[jap]+[lc]

		if lc not in lninvdict:
			lninvdict[lc]=jap

	#print unikill(kill_accents(prevname))," vs ",unikill(kill_accents(thisname))," status: ", status
	pina.write(str(i)+","+thisname+","+jap+","+status+"\n")

bigdict={}

wl_elements=[]

for key in lndict:

	wl_elements=wl_elements+[key]


	if len(lndict[key])>1:
		#lndict.pop(key, None)
		bigdict[key]=lndict[key]

wl_elements=sorted(wl_elements)

wlf=codecs.open("lastname_whitelist.txt",'w', encoding='utf-8', errors='replace')

for x in range(len(wl_elements)):
	wlf.write(str(x+2001)+","+wl_elements[x]+"\n")



json.dump(bigdict, codecs.open("lastnamejson.txt",'w', encoding='utf-8', errors='replace'))		
json.dump(lninvdict, codecs.open("lastnamejson_inv.txt",'w', encoding='utf-8', errors='replace'))	

#LASD-OK BEEPITESE HOLNAP
#KETTOS KARAKTEREKET COLLAPSOLNI EGYEDIRE - ENNEK ALAPJAN SORBARENDEZNI (kovatsch - kovac)