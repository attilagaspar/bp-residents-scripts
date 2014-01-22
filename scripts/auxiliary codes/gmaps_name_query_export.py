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
from time import sleep

import simplekml


lupln="ovic"



from pygeocoder import Geocoder


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


def unikill(str1):

	str2=u""
	for ch in str1:
		try:
			ch2=ch.encode('utf-8')
			str2=str2+ch2
		except:
			pass
	return str2

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

###############################################
wlFile = codecs.open("address_main.txt",'r', encoding='utf-8', errors='replace')

wl=[]

for i in wlFile:
	wl=wl+[i.split("\n")[0].split(',')]

inFile = codecs.open("paired_test.txt",'r', encoding='utf-8', errors='replace')
outFile= codecs.open("name_"+lupln+".csv", "a", encoding="utf-8", errors="replace")
outFile.write("name,address,latitude,longitude,profession\n")




for l in inFile:
	adrlookup=""
	line=l.split("\n")[0].split(",")
	found=0
	try:
		x=int(line[11])
		found=1
	except:
		pass
	if found==1 and int(line[11])<940 and int(line[0])>26188:
		if lupln in japanize(line[1].split()[0]):

			print kill_accents(unikill(line[1]))
			lookup=int(line[11])		
			#print lookup
			#print len(wl[lookup])
			if int(wl[lookup+1][2])==1:
				adrlookup="Budapest, "+kill_accents(line[12])+" utca "+line[13]
			if int(wl[lookup+1][2])==2:
				adrlookup="Budapest, "+kill_accents(line[12])+" ut "+line[13]
			if int(wl[lookup+1][2])==3:
				adrlookup="Budapest, "+kill_accents(line[12])+" ter "+line[13]
			fogl=kill_accents(line[-2])
			print adrlookup.encode("utf-8")
			try:
				results=Geocoder.geocode(adrlookup)
				print results[0]
				outline=line[1]+","+kill_accents(line[12])+" "+line[13]+","+str(results[0].coordinates[0])+","+str(results[0].coordinates[1])+","+fogl	+"\n"
				#outline=kill_accents(line[1])+","+str(results[0].coordinates[0])+","+str(results[0].coordinates[1])+","+fogl	+"\n"
				outFile.write(outline)
				sleep(1)
			except:
				print "zero results"
				pass

#196,Ádám Kálmán,NA, 0, 0, 0, 0, 0, 0, 0,5,180,Döbrentey,,0,1,2,#ok,aut1,Döbrentey-utcza,Döbrentey-u.,posta táv. s. tiszt,I






#kml = simplekml.Kml()
#kml.newpoint(name="kati", coords=[results[0].coordinates])
#kml.save("kati.kml")
