import codecs
# -*- coding:Utf-8 -*-
#coding: utf-8
#RECORD SCRAPER 1.0
#14.41/1/24/2014

#input: CSV

#open file, line by line

#open browser, save file



import mechanize
from bs4 import BeautifulSoup
from process_geo import *
import urllib2
import cookielib
import os
import sys
import time
import codecs

from os import listdir
from os.path import isfile, join


dataurl="http://lear3.bparchiv.hu/kozponti/"

try:
	year = int(sys.argv[1])
except:
	print "invalid year"

dest_dir="../out/archive_raw/"+str(year)+"/records/"
srcfilename="../out/archive_raw/"+str(year)+"/"+str(year)+".csv"

if os.path.isdir(dest_dir)==False:
	os.makedirs(dest_dir)


br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
#br.addheaders =             # [('User-agent', 'Firefox')]

srcfile=codecs.open(srcfilename,"r", encoding="utf-8")
lines=srcfile.readlines()
l=0
for i in lines:
	if u"Fogolytörzskönyv" in i:
		l=l+1


x=0
for i in lines:
	
	row=i.split("\n")[0].split(',')
	for j in range(len(row)):
		row[j]=row[j].strip('"')
	#print row
	#this is for testing purposes
	if row[1]==u"Fogolytörzskönyv":
		print l,"/",x
		finalurl=dataurl+row[-1]
		outfilename=dest_dir+row[-1].split("=")[-1]+".html"
		response = br.open(finalurl)
		pagetext=response.read()
		outfile=open(outfilename,'w')
		outfile.write(pagetext)
		outfile.close()
		time.sleep(1)
		x=x+1
	
