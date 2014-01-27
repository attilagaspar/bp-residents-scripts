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
import operator
import msvcrt
import json
import time
import collections
from time import sleep
from process_geo import *

from pygeocoder import Geocoder

src_file="..\in\geocodev1.csv"

dest_file="..\out\geocodev1_expanded.csv"

src=codecs.open(src_file,"r", encoding="utf-8")
lastid=0
lastno=0
try:
	dest=codecs.open(dest_file,"r", encoding="utf-8")
	
	for line in dest:
		strid=int(line.split(",")[0])
		strno=int(line.split(",")[1])

		if strid>0:
			lastid=strid
			if strno>lastno:
				lastno=strno
	dest.close()
	dest=codecs.open(dest_file,"a", encoding="utf-8")
	

except:
	dest=codecs.open(dest_file,"w", encoding="utf-8")


strtype=[u"utca",u"út",u"tér",u"körút",u"köz"]

x=-1
for line in src:
	x=x+1
	line=line.split("\n")[0]
	l=line.split(";")

	strid=l[0]

	#if int(strid)>=lastid:
	if x>=116: #nyáry pál
		#if int(strid)==lastid:
		#	startval=lastno+1
		#else:
		#	startval=1
		startval=1
		stub=l[1]
		typ=int(l[2])
		full_old=l[3]
		maxno=int(l[4])
		status=l[9]
		
		full_new=full_old
		
		if typ>0 and typ<6:
			full_new=stub+" "+strtype[typ-1]
			#print full_old,full_new
		
		if u"LÁSD" in status:
			full_new=status[4:].split("\n")[0]
			full_new=full_new.rstrip()
		
		for i in range(startval,maxno+1):
			llist=["Budapest",full_new,str(i)]
			lookup=" ".join(llist)
			results=Geocoder.geocode(lookup)
			print len(results),results[0]
			llist=[strid,str(i),full_new,full_old,str(results.coordinates[0]),str(results.coordinates[1])]
			outline=",".join(llist)+"\n"
			#print outline
			dest.write(outline)
			sleep(0.5)






