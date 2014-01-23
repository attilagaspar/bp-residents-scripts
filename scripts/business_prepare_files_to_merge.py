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


srcfilename="../in/BPLAKCIMJEGYZEK_09_1896-1897_cegek.txt"

srcfile = codecs.open(srcfilename,'r', encoding='utf-8', errors='replace')


#these are the names and abbreviations of types of public spaces in Hungarian. (e.g. Street and Str, Square and Sqr. These will help us identify addresses)
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

#if a line starts with one of these characters, that's just some OCR error due to filthy paper
nonstarterlist=[".","^", "="]

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
for i in range(len(lines)):
	if lines[i]!="":
		lines1=lines1+[lines[i]]


#*********************
#STEP 1
#*********************
#WHICH LINE LENGTH INDICATES A NEW OBSERVATION
cutoff=60
#50 for big business (very long lines)
#54 for associations (medium lines)
#60 for small business (very short lines)

masterlist=[]
mlcurr=0
sublist=[]
for i in range(len(lines1)):
	if len(lines1[i])>cutoff:
		sublist=sublist+[lines1[i]]
	else:
		sublist=sublist+[lines1[i]]
		masterlist=masterlist+[sublist]
		#print len(masterlist[-1])
		sublist=[]


#print "master",len(masterlist)

#***********************
#STEP 2
#***********************


for i in range(len(masterlist)):
	for j in range(len(masterlist[i])):
		if j<len(masterlist[i])-1:
			#masterlist[i][j]=masterlist[i][j].split("\n")[0]
			masterlist[i][j]=masterlist[i][j].rstrip()
			if masterlist[i][j][-1]=="-" and  masterlist[i][j+1].split()[0] not in spacestubs:
				masterlist[i][j]=masterlist[i][j][:-1]
#				masterlist[i][j]=masterlist[i][j].split(u"\n")[0]
				

mstr=[]
nms=[]
mnames=[]
assnames=[]
assaddrs=[]
for i in range(len(masterlist)):
	mstr=mstr+["".join(masterlist[i])]
	mstr[i]=u" ".join(mstr[i].split())
	if mstr[i][0] in nonstarterlist:
		mstr[i]=mstr[i][1:]
	assaddrs=assaddrs+["NONE"]
	#################
	#go for addresses
	#################
	# A T)MBSZERKEZET VAN ELBASZVA NEM A KÓD!!!!

	#addrs=re.findall(r"(([A-ZÁÉÍÓÖŐÜŰa-záéíóöőüú\-\— ])+\. +(\d)+([0-9-—])*)",mstr[i],flags=0)
	#print unikill(kill_accents(mstr[i]))
	addrs=re.findall(ur"(([A-ZÁÉÍÓÖŐÜŰa-záéíóöőüú\-\— ])+\.* *(\d)+([0-9\-\—])*)",mstr[i],flags=0)
	#print addrs
	#regexps are found from the back, we are interested in primary addresses
	addrs.reverse()
	adrfound=0
	adrlistlen_prev=len(assaddrs)
	for j in range(len(addrs)):
		if type(addrs[j])==tuple:
			addrs[j]=addrs[j][0]
		
		#print(unikill(kill_accents(addrs[j])))
		#print(unikill(kill_accents(addrs[0])))
		if adrfound==0:
			if type(addrs[j])!=list:
				#print "geci"
				[ptype,pname]=check_if_place(" ".join(addrs[j].split()[:-1]))
				#print (unikill(kill_accents(addrs[j]))),(unikill(kill_accents(str(ptype)))),(unikill(kill_accents(pname)))
				if ptype!=-1:		
						#addr=pname+"-"+space_dict[ptype][0]
						addr=addrs[j]
						assaddrs[-1]=addr
						adrfound==1
			else:
				#print "punci"
				for z in range(len(addrs[j])):
					[ptype,pname]=check_if_place(" ".join(addrs[j][z].split()[:-1]))
					#print (unikill(kill_accents(addrs[j]))),(unikill(kill_accents(str(ptype)))),(unikill(kill_accents(pname)))
					if ptype!=-1 and adrfound!=1:		
						#addr=pname+"-"+space_dict[ptype][0]
						addr=addrs[j][z]
						assaddrs[-1]=addr
						adrfound==1
	
		

	adrlistlen_post=len(assaddrs)
	increment = adrlistlen_post-adrlistlen_prev
	#if increment!=1:
		#print unikill(kill_accents(mstr[i])), "   inc:  ", increment
	#assert adrlistlen_post==adrlistlen_prev+1

			
	#if addr_found_at>-1:

	#	tocheck[j]=tocheck
		#tocheck.pop(j)
		#tocheck.pop(j-1)

	

	#print mstr[i].encode("utf-8")
	#print assaddrs[i].encode("utf-8")
	#names=re.findall(u"([A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú.]+)+", mstr[i], flags=0)

	#duplanevek 
	names1=re.findall(u"([A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú]+[A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú]*)", mstr[i], flags=0)
	for x in range(len(names1)):
		y=re.findall(u"([A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú]+)", names1[x], flags=0)
		names1[x]=" ".join(y)

	#szimplanevek 
	names2=re.findall(u"([A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú]+ [A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú]*)", mstr[i], flags=0)

	names=["noname"]
	if len(names1)>0 or len(names2)>0:
		names=names1+names2

	#If the association is in "Kossuth Lajos street", it will find "Kossuth Lajos" as a person participating, unless...
	newnames=[]
	for zz in range(len(addrs)):
		for z in range(len(names)):
			if names[z] not in addrs[zz]:
				newnames=newnames+[names[z]]
	names=newnames
			

	#print names
	nms=nms+[",".join(names)+"\n"]
	

	mnames=mnames+[names]
	

	#association names are cut from the string
	#to the first dot where the word before the dot is longer than 3 chars

	assname_elements=mstr[i].split('.')
	#print unikill(kill_accents(mstr[i]))
	endpos=0
	if len(assname_elements)>1:
		for z in range(len(assname_elements)):
			#print len(assname_elements),z,len(assname_elements[z].split())
			if len(assname_elements[z].split())>1:
				checkword=assname_elements[z].split()[-1]
			else:
				checkword=assname_elements[z]
			if len(checkword)>3:
				endpos=z
	if endpos==0:
		endpos=3
	assn=".".join(assname_elements[:endpos])
		
	#commas in association names mess up the CSV. let's get rid of them.
	assn=" ".join(assn.split(","))
	#let's get rid of extra spaces as well
	assn=" ".join(assn.split())
	#print unikill(kill_accents(assn))
	assnames=assnames+[assn]

#assert len(assaddrs)==len(assnames)

outfile=codecs.open("../out/out.txt",'w', encoding='utf-8', errors='replace')
outfilex=codecs.open("../out/assadrs.txt",'w', encoding='utf-8', errors='replace')
outfiley=codecs.open("../out/assnames.txt",'w', encoding='utf-8', errors='replace')
outfilez=codecs.open("../out/master.txt",'w', encoding='utf-8', errors='replace')
for x in range(len(assaddrs)):
	outfilex.write(assaddrs[x]+"\n")
for x in range(len(assnames)):
	outfiley.write(assnames[x]+"\n")
for x in range(len(mstr)):
	outfilez.write(mstr[x]+"\n")


outfile2=codecs.open("../out/business_csv_master.txt",'w', encoding='utf-8', errors='replace')
outfile2.write("associd,assocname,assocaddr,fullname,nkey1,nkey2,jap1,jap2\n")


allnames=[]

src_people=[]
for i in range(len(nms)):
	for j in range(len(mnames[i])):
		src_people_unit=[str(i), assnames[i], mnames[i][j]]
		if japanize(mnames[i][j].split()[0]) not in allnames:
			allnames=allnames+[japanize(mnames[i][j].split()[0])]
		src_people=src_people+[src_people_unit]
		lwrcase=kill_accents(mnames[i][j]).split()
		jap2=[]
		for z in mnames[i][j].split():
			jap2=jap2+[japanize(z)]
			#print jap2[-1]
			#assert japanize(z)[-1]!="y"
		
		if len(lwrcase)<2: 
			lwrcase=lwrcase+[""]
		if len(jap2)<2:
			jap2=jap2+[""]

		assert len(lwrcase)==2
		assert len(jap2)==2


		person=",".join([str(i), assnames[i], assaddrs[i], mnames[i][j]]+lwrcase[0:2]+jap2[0:2])+"\n"
		person="".join(person.split('"'))
		outfile2.write(person.encode("utf-8").decode("utf-8"))

for i in range(len(masterlist)):
	outfile.write("\n")
	outfile.write("\n")
	outfile.write(mstr[i].encode("utf-8").decode("utf-8"))

print "master data ready"
print "number of surnames: ",len(allnames)

