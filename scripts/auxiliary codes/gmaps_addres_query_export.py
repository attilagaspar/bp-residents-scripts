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

lookup=414
lupln=""
lupsstr=""


from pygeocoder import Geocoder

def unikill(str1):

	str2=u""
	for ch in str1:
		try:
			ch2=ch.encode('utf-8')
			str2=str2+ch2
		except:
			pass
	return str2



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
	
	return "".join(retstring)


wlFile = codecs.open("address_main.txt",'r', encoding='utf-8', errors='replace')

wl=[]

for i in wlFile:
	wl=wl+[i.split("\n")[0].split(',')]

inFile = codecs.open("paired_test.txt",'r', encoding='utf-8', errors='replace')
outFile= codecs.open("street_"+str(lookup)+".csv", "a", encoding="utf-8", errors="replace")
#outFile.write("name,address,latitude,longitude,profession\n")
#business_geocoder = Geocoder('gHIwdUSCdv20P2zxsWWCH2YA', 'AIzaSyCNEp66ef18uMs4vvTXzqM8ye3iXtyEzy0')
#business_geocoder = Geocoder('AIzaSyCNEp66ef18uMs4vvTXzqM8ye3iXtyEzy0', 'gHIwdUSCdv20P2zxsWWCH2YA')
#business_geocoder = Geocoder("523352502057", 'AIzaSyCNEp66ef18uMs4vvTXzqM8ye3iXtyEzy0')

#### EZT HOGY A FASZOMBA ETETEM MEG VELE

print len(wl[lookup])

checkednumbers=[]
checkedlat=[]
checkedlon=[]

no=0

for l in inFile:
	no=no+1
	adrlookup=""
	line=l.split("\n")[0].split(",")
	found=0
	try:
		x=int(line[11])
		found=1
	except:
		pass
	if found==1:
		if int(line[11])==lookup and line[13]!="" and no>56035:
			
					
			print unikill(kill_accents(l))
			if int(line[13]) not in checkednumbers:
				
				checkednumbers=checkednumbers+[int(line[13])]
				if int(wl[lookup+1][2])==1:
					adrlookup="Budapest, "+kill_accents(line[12])+" utca "+line[13]
				if int(wl[lookup+1][2])==2:
					adrlookup="Budapest, "+kill_accents(line[12])+" ut "+line[13]
				if int(wl[lookup+1][2])==3:
					adrlookup="Budapest, "+kill_accents(line[12])+" ter "+line[13]
				fogl=kill_accents(line[-2])
				print adrlookup.encode("utf-8")

				m = len(adrlookup)%3
				adrlookup=adrlookup+(3-m)*" "
				print len(adrlookup)
				#results=business_geocoder.geocode(adrlookup)


				results=Geocoder.geocode(adrlookup)
				checkedlat=checkedlat+[results.coordinates[0]]
				checkedlon=checkedlon+[results.coordinates[1]]
				print results[0]
				outline=line[1]+","+kill_accents(line[12])+" "+line[13]+","+str(results[0].coordinates[0])+","+str(results[0].coordinates[1])+","+fogl	+"\n"
				#outline=kill_accents(line[1])+","+str(results[0].coordinates[0])+","+str(results[0].coordinates[1])+","+fogl	+"\n"
				outFile.write(outline)
				sleep(1)
			else: 
				numb = line[13]
				index = checkednumbers.index(int(numb))
				lat = str(checkedlat[index])
				lon = str(checkedlon[index])
				fogl=kill_accents(line[-2])
				outline=line[1]+","+kill_accents(line[12])+" "+line[13]+","+lat+","+lon+","+fogl	+"\n"
				#outline=kill_accents(line[1])+","+lat+","+lon+","+fogl	+"\n"
				outFile.write(outline)

#196,Ádám Kálmán,NA, 0, 0, 0, 0, 0, 0, 0,5,180,Döbrentey,,0,1,2,#ok,aut1,Döbrentey-utcza,Döbrentey-u.,posta táv. s. tiszt,I






#kml = simplekml.Kml()
#kml.newpoint(name="kati", coords=[results[0].coordinates])
#kml.save("kati.kml")
