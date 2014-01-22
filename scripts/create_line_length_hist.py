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
#from fuzzywuzzy import fuz
import operator
import msvcrt
import json

from process_basics import *
from process_geo import *


srcfilename="../in/BPLAKCIMJEGYZEK_09_1896-1897_cegek_kicsi.txt"

srcfile = codecs.open(srcfilename,'r', encoding='utf-8', errors='replace')


space_dict=[[u"-utcza", u" utcza", u"-u.", u"-utca"],
[u" út", u"-út"],
[u"-tér"],
[u" körút", u"-körút"],
[u"-köz"],
[u"sor"],
[u" rakpart", u"-rakpart"],
[u"-lépcső"]]

space_errors=[[u"-u",u"-u",u"-n.",u"irtcza",u"-a.",u" u ",u"ufeza",u"-ii",u"-ri",u"ntcza",u"-ú ",u"-ia",u"-it."],
[u"iít",u"-rit",u"-fit",u"-vit",u"-írt",u"-iit",u"-iát",u"-ut",u"-i.t",],
[u"téi",u"tér",u"tere",u"-té ",u"-tór"],
[u"korut",u"korút",u"körut",u"körüt",u"könít",u"körrit ",u"körfit",u"körvit",u"körú",u"köriit",u"könit",u"kör-lít",u"kör- lít",u"krt"],
[u"-koz"],
[u"-sör"],
[u"rakp",u"rak- part",u"rakn.",u"-rpt",u"rkp",u"ratp",u"-rp."],
[u"-lpcsso"]]


spacestubs=[u"utcza", u"út",u"tér",u"körút",u"koz",u"köz",u"u.",u"n.",u"irtcza",u"a.",u"ufeza",u"ntcza",u"it.",u"téi",u"-tór",u"korut",u"korút",u"körut",u"körüt",u"könít",u"körrit ",u"körfit",u"körvit",u"körú",u"köriit",u"könit",u"kör-lít",u"kör- lít",u"krt"]

lines=srcfile.readlines()

print "number of lines in source text: ",len(lines)




#******************
#STEP 0
#******************

#kill "lonely" lines
for i in range(len(lines)):
	if i>0 and i<len(lines)-1:
		#if lines[i-1]==u"\n" and lines[i+1]==u"\n":
		if len(lines[i-1])<3 and len(lines[i+1])<3:			
			lines[i]=""
#kill very short lines and empty lines
for i in range(len(lines)):
	if i<len(lines) and lines[i].strip()==u"":
		lines[i]=""
	if i<len(lines) and len(lines[i])<4:
		lines[i]=""

lines1=[]
lengths=0
for i in range(len(lines)):
	if lines[i]!="":
		lines1=lines1+[lines[i]]
		if len(lines[i])>lengths:
			lengths=len(lines[i])

hist=[0]*140
print "max line length= ",lengths
for i in range(len(lines1)):
	hist[len(lines1[i])]=hist[len(lines1[i])]+1

histfile=codecs.open("../out/cegek_hist.txt",'w', encoding='utf-8', errors='replace')
for i in range(len(hist)):
	histfile.write(str(i)+","+str(hist[i])+"\n")