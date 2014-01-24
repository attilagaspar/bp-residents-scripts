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


allkeys=[]
master=[]


try:
	year = int(sys.argv[1])
except:
	print "invalid year"

dest_dir="../out/archive_raw/"+str(year)+"/"
src_dir="../out/archive_raw/"+str(year)+"/records/"
outfilename1=dest_dir+str(year)+"_records.csv"
outfile=codecs.open(outfilename1,"w", encoding="utf-8")

files = [ f for f in listdir(src_dir) if isfile(join(src_dir,f)) ]

print len(files)



#WHAT WE ARE LOOKING FOR:
#labeled stuff:
#<td class="label">

#print soup
x=0
for f in files:
	
	if x%100==0:
		print x

	fname=src_dir+f
	infile=open(fname,'r')
	soup = BeautifulSoup(infile.read())


	persondict={}
	labels=soup.find_all('td', recursive=True)
	for i in range(len(labels)):
		if "class" in labels[i].attrs:
			
			if labels[i]['class']==["label"]:
				labelname=labels[i].text.strip()
				if labelname not in allkeys:
					allkeys=allkeys+[labelname]
				labelvalue=labels[i].next_sibling.next_sibling.text.strip()
				persondict[labelname]=labelvalue

	#locations
	locs=soup.find_all('tr', recursive=True)
	y=0
	for i in range(len(locs)):
		if "class" in locs[i].attrs:
			if locs[i]['class']==["main"]:
				if y==0:
					bplace=locs[i+1].find_all('th')
					#print bplace
					bplaceval=locs[i+2].find_all('td')
					#print len(bplace),",",len(bplaceval)
					for j in range(len(bplace)):
						labelname="bplace_"+bplace[j].text
						if labelname not in allkeys:
							allkeys=allkeys+[labelname]
						labelvalue=bplaceval[j].text
						persondict[labelname]=labelvalue
					y=y+1
				#current residence
				if y==1:
					curplace=locs[i+1].find_all('th')
					curplaceval=locs[i+2].find_all('td')
					#print len(curplace),",",len(curplaceval)
					for j in range(len(curplace)):
						labelname="curplace_"+curplace[j].text
						if labelname not in allkeys:
							allkeys=allkeys+[labelname]
						labelvalue=curplaceval[j].text
						persondict[labelname]=labelvalue

	master=master+[persondict]
	x=x+1

	#location data

header=",".join(allkeys)+"\n"
outfile.write(header)

for i in range(len(master)):
	pd=master[i]
	rowlist=[]
	for j in range(len(allkeys)):
		if allkeys[j] in pd.keys():
			rowlist=rowlist+[pd[allkeys[j]]]
		else:
			rowlist=rowlist+["N/A"]
	row=",".join(rowlist)+"\n"
	outfile.write(row)