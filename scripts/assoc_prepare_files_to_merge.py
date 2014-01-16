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


srcfilename="../in/BPLAKCIMJEGYZEK_09_1896-1897_egyesuletek.txt"

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
for i in range(len(lines)):
	if lines[i]!="":
		lines1=lines1+[lines[i]]

hist=[0]*90
for i in range(len(lines1)):

	hist[len(lines1[i])]=hist[len(lines1[i])]+1

histfile=codecs.open("../out/hist.txt",'w', encoding='utf-8', errors='replace')
for i in range(len(hist)):
	histfile.write(str(i)+","+str(hist[i])+"\n")

#*********************
#STEP 1
#*********************
cutoff=54

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

	#################
	#go for addresses
	#################
	
	#addrs=re.findall(r"(([A-ZÁÉÍÓÖŐÜŰa-záéíóöőüú\-\— ])+\. +(\d)+([0-9-—])*)",mstr[i],flags=0)
	addrs=re.findall(ur"(([A-ZÁÉÍÓÖŐÜŰa-záéíóöőüú\-\— ])+\.* *(\d)+([0-9\-\—])*)",mstr[i],flags=0)
	#print addrs
	adrfound=0
	for j in range(len(addrs)):
		if type(addrs[j])==tuple:
			addrs[j]=addrs[j][0]
		#print(unikill(kill_accents(addrs[j])))
		[ptype,pname]=check_if_place(" ".join(addrs[j].split()[:-1]))

		if ptype!=-1:
			if adrfound==0:
				addr=pname+"-"+space_dict[ptype][0]
				assaddrs=assaddrs+[addr]
				adrfound==1
	if adrfound==0:
		if len(addrs)>0:
			print(unikill(kill_accents(addrs[0])))
		assaddrs=assaddrs+["NONE"]


			
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


	names=names1+names2

	#print names
	nms=nms+[",".join(names)+"\n"]
	mnames=mnames+[names]

	#association names
	assn=re.findall(u"^[^,.]+",mstr[i],flags=0)[0][:-1]
	#print assn.encode("utf-8")
	assnames=assnames+[assn]


outfile=codecs.open("../out/out.txt",'w', encoding='utf-8', errors='replace')

outfile2=codecs.open("../out/assoc_csv_master.txt",'w', encoding='utf-8', errors='replace')
outfile2.write("associd,assocname,assocaddr,fullname,nkey1,nkey2\n")
outfile3=codecs.open("../out/assoc_csv_using.txt",'w', encoding='utf-8', errors='replace')
outfile3.write("person,personname,nkey1,nkey2,ad1,ad2,ad3,ad4\n")

allnames=[]

src_people=[]
for i in range(len(nms)):
	for j in range(len(mnames[i])):
		src_people_unit=[str(i), assnames[i], mnames[i][j]]
		if japanize(mnames[i][j].split()[0]) not in allnames:
			allnames=allnames+[japanize(mnames[i][j].split()[0])]
		src_people=src_people+[src_people_unit]
		lwrcase=kill_accents(mnames[i][j]).split()
		person=",".join([str(i), assnames[i], assaddrs[i], mnames[i][j]]+lwrcase)+"\n"
		outfile2.write(person.encode("utf-8").decode("utf-8"))

for i in range(len(masterlist)):
	outfile.write("\n")
	outfile.write("\n")
	outfile.write(mstr[i].encode("utf-8").decode("utf-8"))

print "master data ready"
print "number of surnames: ",len(allnames)

#reading names

dest_people=[]
namesrc=codecs.open("../in/paired_test.txt",'r', encoding='utf-8', errors='replace')
for namelines in namesrc:
	nl = namelines.split("\n")[0].split(",")

	nkeys=[""]*2
	nk=kill_accents(nl[1]).split()
	try:
		nkeys[0]=nk[0]
		nkeys[1]=nk[1]
	except:
		pass

	
	nlint = [nl[0]]+[nl[1]]+nk+nl[11:15]
	#if japanize(nlint[1]) in allnames:
	#	dest_people=dest_people+[nlint]
	#dest_people=dest_people+[nlint]
	outfile3.write(",".join(nlint)+"\n")


print "using data ready"
#print "number of candidates:",len(dest_people)

#for i in range(len(src_people)):
#	if i%100==0:
#		print i
#	last=src_people[i][2].split()[0]
#	first=src_people[i][2].split()[1]
#	cands=[]
#	for j in range(len(dest_people)):
#		if japanize(last)==japanize(dest_people[j][1]):
#			cands=cands+[dest_people[j]]
#	if len(cands)!=0:
#		sim=[]
#		for j in range(len(cands)):
#			sim=sim+[difflib.SequenceMatcher(None,first,cands[j][2]).ratio()]
#	
#		bestindex=sim.index(max(sim))
#		src_people[i]=src_people[i]+cands[bestindex]
#	else:
#		src_people[i]=src_people[i]+["fail"]
#	outfile3.write(",".join(src_people[i]).encode("utf-8").decode("utf-8")+"\n")





#nevsorok: id, vezetek, kereszt, cimkodok