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

space_dict=[[1,["-utcza", " utcza", "-u.", "-utca","-u ","-n.","irtcza","-a."," u ","ufeza","-ii","-ri","ntcza","-ú ","-ia","-it."]],
[2,[" út", "-út","iít","-rit","-fit","-vit","-írt","-iit","-iát","-ut","-i.t"]],
[3,["-tér","téi","tér","tere","-té ","-tór"]],
[4,[" körút", "-körút","korut","korút","körut","körüt","könít","körrit ","körfit","körvit","körú","köriit","könit","kör-lít","kör- lít","krt"]],
[5,["-köz","-koz"]],
[6,["sor","-sör"]],
[7,[" rakpart", "-rakpart","rakp","rak- part","rakn.","-rpt","rkp","ratp","-rp."]],
[8,["-lépcső","-lpcsso"]]]

for i in range(len(space_dict)):
	space_dict[i][1] = [j.decode('UTF-8') if isinstance(j, basestring) else j for j in space_dict[i][1]]

unicode(space_dict)

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


# FUNCTIONS

def isDistrict(instring):
	districts = ["0", " I", " II"," III"," IV"," V"," VI"," VII"," VIII"," IX"," X"]
	retval=0
	for i in range(len(districts)):
		if instring==districts[i]:
			retval=i
	return retval



wlFileName="Ujpest_utca_jegyzek.csv"
wlFile = codecs.open(wlFileName,'r', encoding='utf-8', errors='replace')

cleanFileName="address_whitelist_ujpest.txt"
cleanFile = codecs.open(cleanFileName,'w', encoding='utf-8', errors='replace')

idSpace = 1

for line in wlFile:
	print line.encode("utf-8")
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
			print type(space_dict[i][1][j]), type(address)
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

	#ll=[str(idSpace),nameStub,str(spaceType),address,str(distr1),str(distr2),des_string,res_string,"\n"]
	ll=[str(2000+idSpace),nameStub,str(spaceType),address,"99","99"]
	outline=",".join(ll)+"\n"
	cleanFile.write(outline)
	idSpace=idSpace+1


