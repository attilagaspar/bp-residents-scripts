#RECORDLIST COLLAPSER 1.0
#14.41/1/24/2014

#input: year

#get directory

#list files in directory, go through them

#find records, write them out in CSV

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


try:
	year = int(sys.argv[1])
except:
	print "invalid year"

dest_dir="../out/archive_raw/"+str(year)+"/"
outfilename1=dest_dir+str(year)+".csv"
outfile=codecs.open(outfilename1,"w", encoding="utf-8")

files = [ f for f in listdir(dest_dir) if isfile(join(dest_dir,f)) ]

print len(files)
x=0
for fname in files:
	if x%10==0:
		print "file: ",x
	filename=dest_dir+fname
	infile=open(filename,'r')
	soup = BeautifulSoup(infile.read())
	oddrows=soup.find_all('tr', class_="odd", recursive=True)
	evenrows=soup.find_all('tr', class_="even", recursive=True)
	rows=oddrows+evenrows

	#print "pina"
	#print len(rows)

	for i in range(len(rows)):
		rowlist=[]
		if len(rows[i])>0:
			rowels=rows[i].find_all('td')
			#print rows[i].td
			#print rows[i].td.text

			#print rowels
			for j in range(len(rowels)):
				try:
					rowlist=rowlist+[rowels[j].ul.li.a['href']]
				except:
					rowlist=rowlist+[rowels[j].text]

				#print "geci"
				#if 'class' in rowels[j].attrs:
				#	if rowels[j]['class']=="b":
				#		#if link
				#		print rowels[j].ul.li.a['href']
				#		rowlist=rowlist+[rowels[j].ul.li.a['href']]
				#		
				#	else:
				#		#if not link
				#		rowlist=rowlist+[rowels[j].text]
				#else:
				#	rowlist=rowlist+[rowels[j].text]
		for j in range(len(rowlist)):
			rowlist[j]=rowlist[j].split("\n")[0]
			rowlist[j]=rowlist[j].strip()
			rowlist[j]='"'+rowlist[j]+'"'
		row=",".join(rowlist)+"\n"
		outfile.write(row)
	x=x+1



