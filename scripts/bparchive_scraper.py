#ARCHIVE LIST SCRAPER 1.0
#14.41/1/24/2014

#input: year


#start mechanize, go archive searcher
#source http://lear3.bparchiv.hu/kozponti/advancedsearch.html

#initialize search, year=input
#create subdir if it does not exist

#send form
#save page, press next
#wait 2 secs, repeat

import mechanize
from bs4 import BeautifulSoup
from process_geo import *
import urllib2
import cookielib
import os
import sys
import time

source_url="http://lear3.bparchiv.hu/kozponti/advancedsearch.html"

try:
	year = int(sys.argv[1])
except:
	print "invalid year"


br = mechanize.Browser()
#br.set_all_readonly(False)    # allow everything to be written to
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
#br.addheaders =             # [('User-agent', 'Firefox')]


response = br.open(source_url)
mainpage=response.read()      # the text of the page

br.form = list(br.forms())[0] 

#control1 = br.form.find_control("controlname")

controlset="Azonosito/KozpontiIdo"
dest_dir="../out/archive_raw/"+str(year)

control1=br.form.find_control("conditions[0].qualifier")
control1.value=[controlset]

control2=br.form.find_control("conditions[0].text")
control2.value=str(year)

response = br.submit()

#SCRAPING STARTS

if os.path.isdir(dest_dir)==False:
	os.makedirs(dest_dir)


pagetext=response.read()
hkey="latok sz"
ekey="&nbsp"
hpos=pagetext.find(hkey)+len(hkey)+5
text1=pagetext[hpos:hpos+20]
header=text1.split(ekey)[0]
print header	

hkey="latok: "
ekey=" oldal"
hpos=pagetext.find(hkey)+len(hkey)
text1=pagetext[hpos:hpos+20]
current=text1.split(ekey)[0]+")"
c=current.split("(")[1].split(".")[0]
print current
dyn_filename=dest_dir+"/"+str(year)+"_"+"0000"+".html"


outfile=open(dyn_filename,'w')
outfile.write(pagetext)

still_searching=1

pnoold=0
while still_searching:
	time.sleep(1)
	goon=0
	for link in br.links():
		if "foundpage.html?page=" in link.url:
			pno=link.url.split("page=")[-1]
			if int(pno)>pnoold:
				goon=1
	if goon==0:
		still_searching=0
	for link in br.links():
		if "foundpage.html?page=" in link.url:
			pno=link.url.split("page=")[-1]
			if int(pno)>pnoold:
				print "going on"
				pnoold=pnoold+1
				break
		#else:
		#	still_searching=0
	#print "itt vagyok"
	#print link.url
	#print still_searching
	if still_searching==1:
		#print "itt is"
		response=br.follow_link(link)
		hkey="latok: "
		ekey=" oldal"
		pagetext=response.read()
		hpos=pagetext.find(hkey)+len(hkey)
		text1=pagetext[hpos:hpos+20]
		current=text1.split(ekey)[0]+")"
		c=str(pnoold)
		c="0"*(4-len(c))+c
		print current
		dyn_filename=dest_dir+"/"+str(year)+"_"+c+".html"
		print dyn_filename
		outfile=open(dyn_filename,'w')
		outfile.write(pagetext)
		still_searching=1