import codecs
#coding: utf-8
# -*- coding:Utf-8 -*-

import locale
import csv
import os
import sys
import re
from msvcrt import getch
import difflib


# WHITELIST OBJECTS

space_dict=[[1,["-utcza", " utcza", "-u.", "-utca"]],
[2,[" út".encode('utf-8'), "-út"]],
[3,["-tér"]],
[4,[" körút", "-körút"]],
[5,["-köz"]],
[6,["sor"]],
[7,[" rakpart", "-rakpart"]],
[8,["-lépcső"]]]

#codesFileName="white.txt"
#codesFile = codecs.open(codesFileName,'r', encoding='utf-8', errors='replace')
#no=0
#space_dict=[]
#for line in codesFile:
#	line.lstrip()
#	line=line.split("\n")[0]
#	line=line.split("\r")[0]
#	line=line.split("\ufeff")[0]
#	llist=line.split(',')
#	space_dict=space_dict+[[no,llist]]

print space_dict



space_erros=[["-u ","-n.","irtcza","-a."," u ","ufeza","-ii","-ri","ntcza","-ú ","-ia","-it."],
["iít","-rit","-fit","-vit","-írt","-iit","-iát","-ut","-i.t",],
["téi","tér","tere","-té ","-tór"],
["korut","korút","körut","körüt","könít","körrit ","körfit","körvit","körú","köriit","könit","kör-lít","kör- lít","krt"],
["-koz"],
["-sör"],
["rakp","rak- part","rakn.","-rpt","rkp","ratp","-rp."],
["-lpcsso"]]


# FUNCTIONS

def isDistrict(instring):
	districts = ["0", " I", " II"," III"," IV"," V"," VI"," VII"," VIII"," IX"," X"]
	retval=0
	for i in range(len(districts)):
		if instring==districts[i]:
			retval=i
	return retval



wlFileName="Budapest_utca_jegyzek.txt"
wlFile = codecs.open(wlFileName,'r', encoding='utf-8', errors='replace')

cleanFileName="address_whitelist.txt"
cleanFile = codecs.open(cleanFileName,'w', encoding='utf-8', errors='replace')

idSpace = 1

for line in wlFile:
	line=line.split("\n")[0]
	line=line.split("\r")[0]

	res_string=u""
	des_string=u""
	nameStub=u"NOMATCH"
	spaceType=0
	distr1=0
	distr2=0
	
	lineElements = line.split(",")
	address = lineElements[0]
	for i in range(len(space_dict)):
		for j in range(len(space_dict[i][1])):
			#print space_dict[i][1][j].decode('utf-8')
			if space_dict[i][1][j] in address:
				#print space_dict[i][1][j].encode('utf-8')
				spaceType=i
				nameStub=address.split(space_dict[i][1][j])[0]

	if spaceType==0:
		print(line).encode('utf-8')
		#print("ERROR: spaceType could not be matched")
		#print("\n")
	
	currentCol=0
	while currentCol<len(lineElements)-1:
		currentCol=currentCol+1
		disflag=0
		desflag=0
		if distr1==0 or distr2==0:
			distr=isDistrict(lineElements[currentCol])
			if distr1==0 and distr!=0:
				distr1=distr
				disflag=1
			elif distr2==0 and distr!=0:
				distr2=distr
				disflag=1
		if u"(" and u")" in lineElements[currentCol] :		
			desflag=1
			des_string=lineElements[currentCol]
			des_string.lstrip()
			try:
				des_string=des_string.split("(")[1]
			except:
				pass
			try:
				des_string=des_string.split(")")[0]
			except:
				pass
			#des_string=des_string.translate(None,'()')
		if disflag==0 and desflag==0:
			rs=lineElements[currentCol]
			rs=" ".join(rs.split())
			rs=".".join(rs.split("."))
			res_string=res_string+rs
	#ll=[str(idSpace),nameStub,str(spaceType),address,str(distr1),str(distr2),des_string,res_string,"\n"]
	ll=[str(idSpace),nameStub,str(spaceType),address,str(distr1),str(distr2)]
	outline=",".join(ll)+"\n"
	cleanFile.write(outline)
	idSpace=idSpace+1


