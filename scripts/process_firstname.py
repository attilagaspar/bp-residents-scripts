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
from fuzzywuzzy import fuzz
import operator
import msvcrt
import json
import time
import collections

from process_basics import *





def collapse_namelist(inFileName,colNo):

	inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')
	names = []
	accentednames=[]
	re.U
	asszony=0
	for lines in inFile:
		if len(lines.split(",")[1].split())>colNo:
			string = lines.split(",")[1].split()[1]
			rxp=re.compile(u"[A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú.]*")
			if string[-2:]==u"né" or string[-2:]==u"ne":
				asszony=asszony+1
				string=string[:-3]
				if len(string)>=1 and string[-1]=="-":
					string=string[:-2]
			if rxp.match(string):
				names=names+[kill_accents(string).lower()]
				#names=names+[unidecode(string)]
				accentednames=accentednames+[string]

	
	#namelist=list(set(sorted(names))).sort()
	#namelist = sorted(list(set(names)))
	namelist = sorted(dupl_drop(names))
	print "length of namelist is ",len(namelist)
	return namelist


def build_correctand(inFileName):
	# reading and sorting names from input file
	allnames_1 = collapse_namelist(inFileName,1)
	#print allnames_1
	print "elso oszlop ",len(allnames_1)
	allnames_2 = collapse_namelist(inFileName,2)
	print "masodik oszlop ",len(allnames_2)

	allnames=allnames_1
	for i in allnames_2:
		if i not in allnames_1:
			allnames=allnames+[i]
	return allnames

def name_preprocess(str1):
		str2=str1
		gender_override="0"
		if str1[-2:]=="ne":
			str2 = str1[:-2]
			gender_override="2"
			if len(str2)>=1:
				if str2[-1]=="-":
					
					str2=str2[:-1]
				#if len(str2)>=1 and str2[-1]==".":
					#str2=str2[:-1]					
			#print "waifu",str1,str2
		# IF IT IS ABBREVIATED NORMAL NAME - mark 2
		while len(str2)>=1 and str2[-1]==".":
			str2=str2[:-1]
			#print "abbr",str1, str2

		return [str2,gender_override]


def dict_freqdist(namedict,toclean):
	freq=[]
	fdist=[]
	tocorr = codecs.open(toclean,'r', encoding='utf-8', errors='replace')
	allnames=tocorr.read().split(",")
	print "total number of potential names:",len(allnames)
	#print allnames[-1].encode('utf-8')
	for i in allnames:
		i=name_preprocess(kill_accents(i))[0]
		if i not in freq:
			if i in namedict:
				if namedict[i][0]!="ABBR" and namedict[i][0]!="SKIP" and namedict[i][0] not in freq:
					#print "genya"
					freq=freq+[namedict[i][0]]
					fdist=fdist+[1]
		elif i in freq:
			fdist[freq.index(i)]=fdist[freq.index(i)]+1
	print "total number of eventual names:",len(freq),len(fdist)
	return [freq,fdist]


def lookup_best(str1,freq,fdist):
	#print str1
	matches=[0]*len(freq)
	for i in range(len(freq)):
		if len(str1)<len(freq[i]):
			#print freq[i]
			if freq[i].startswith(str1):
				matches[i]=1
	#print matches
	rel = []
	reldist = []
	for i in range(len(freq)):
		if matches[i]==1:
			rel=rel+[freq[i]]
			reldist=reldist+[fdist[i]]
	#print reldist
	if len(reldist)==0:
		return "SKIP"
	else:
		best = max(reldist)
		str2 = rel[reldist.index(best)]
		return str2





def fname_dict_create(inFileName, wlFileName):

	#this function builds a dictionary of first name corrections

	inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')

	#collect all first names from the input file
	allnames=build_correctand(inFileName)
	print allnames

	wlFile = codecs.open(wlFileName,'r', encoding='utf-8', errors='replace')

	#collect name processing commands from file or start a new one
	try:
		proba = codecs.open("nameclean_comms.txt","a",encoding='utf-8', errors='replace')
	except:
		proba = codecs.open("nameclean_comms.txt","w",encoding='utf-8', errors='replace')
	proba.close()
	proba = codecs.open("nameclean_comms.txt","r",encoding='utf-8', errors='replace')
	processednames = []
	processedcomms = []
	processedgender = []
	processedid = []
	for lines in proba:
		processednames=processednames+[lines.split(",")[0]]
		processedcomms=processedcomms+[lines.split(",")[1]]
		processedgender=processedgender+[lines.split(",")[2].split("\n")[0]]
	proba.close()
	print processednames
	namedict = {'void':'void'}


	# reading and sorting names from whitelist by gender
	malenames=[]
	malenames_ind=[]
	femnames=[]
	femnames_ind=[]

	for i in wlFile:
		i=i.split("\n")[0]
		
		line=i.split(",")
		
		if "1" in line[2]:
			malenames=malenames+[line[1]]
			malenames_ind=malenames_ind+[int(line[0])]
			
		if "2" in line[2]:
			femnames=femnames+[line[1]]
			femnames_ind=femnames_ind+[int(line[0])]
	
	malenames_orig=malenames
	femnames_orig=femnames
	addednames = 700

	#if a new name is given as part of the process
	for i in range(len(processednames)):

		if (processedcomms[i] not in malenames) and (processedcomms[i] not in femnames):
			if processedcomms[i]!="ABBR" and processedcomms[i]!="SKIP":
				if processedgender[i]=="1":
					malenames=malenames+[processedcomms[i]]
					malenames_ind=malenames_ind+[str(addednames)]
					addednames=addednames+1
				elif processedgender[i]=="2":
					femnames=femnames+[processedcomms[i]]
					femnames_ind=femnames_ind+[str(addednames)]
					addednames=addednames+1


	print "no of male names: ",len(malenames)
	print "no of female names: ",len(femnames)


	
	indic = []
	gender = []
	names_resid = []


	for i in range(len(allnames)):
		namenf=1
		lowfname = allnames[i]
		# IF IT HAS NORMAL MALE NAME - mark 1
		if  lowfname in malenames:
			indic=indic+[1]
			gender = gender + [1]
			namenf=0
		# IF IR HAS NORMAL FEMALE NAME - mark 1
		elif lowfname in femnames:
			indic=indic+[1]
			gender = gender + [2]
			namenf=0
		# IF IT IS A NORMAL MRS MALE NAME - mark 1 
		elif lowfname[-2:]=="ne":
			husname = lowfname[:-3]
			if len(husname)>=1 and husname[-1]=="-":
				husname=husname[:-2]
			if husname[-1]!=".":
				if husname in malenames:
					indic = indic+[1]
					gender = gender+[2]
					namenf=0

			else: # ABBREVIATION - mark 2
				indic=indic+[2]
				gender=gender+[0]
				namenf=0
		# IF IT IS ABBREVIATED NORMAL NAME - mark 2
		elif lowfname[-1]==".":
			gender=gender+[0]
			indic=indic+[2]
			namenf=0


		if namenf==1:

			if lowfname not in processednames:	
				
				mnamematch=[]
				for x in range(len(malenames)):
					mnamematch=mnamematch+[difflib.SequenceMatcher(None,lowfname,malenames[x]).ratio()]
				fnamematch=[]
				for x in range(len(femnames)):
					fnamematch=fnamematch+[difflib.SequenceMatcher(None,lowfname,femnames[x]).ratio()]

				bestmale = malenames[mnamematch.index(max(mnamematch))]
				bestfem = femnames[fnamematch.index(max(fnamematch))]
				
				print lowfname.encode("utf-8"),bestmale,max(mnamematch),bestfem,max(fnamematch)
				print ("1: MALE, 2: FEMALE, 3: ABBREV, 4: SKIP, 5: NEW MALE, 6: NEW FEMALE")
				
				cmdchar=wait_command(3)
				if not cmdchar:
					if max([max(mnamematch),max(fnamematch)])>=0.8:				
						if max(fnamematch)>max(mnamematch):
							cmdchar="2"
						else:
							cmdchar="1"
					elif len(lowfname)<5:
						cmdchar="3"
					else:							
						cmdchar = "4"
				
				if cmdchar=="`":
					ovr = raw_input("override:")
					if ovr in malenames:
						gender= gender+[1]
						indic = indic + [3]
						matches=",".join([lowfname,malenames[malenames.index(ovr)],"1"])+"\n"
					elif ovr in femnames:
						gender= gender+[2]
						indic = indic + [3]
						matches=",".join([lowfname,femnames[femnames.index(ovr)],"2"])+"\n"
					else:
						matches=ovr+",override but no match,0\n"
				if cmdchar=="1":
					gender = gender+[1]
					indic = indic + [3]
					matches=",".join([lowfname,bestmale,"1"])+"\n"
				if cmdchar=="2":
					gender = gender+[2]
					indic = indic + [3]
					matches=",".join([lowfname,bestfem,"2"])+"\n"
				if cmdchar=="4":
					gender = gender+[0]
					indic = indic + [0]
					matches=",".join([lowfname,"SKIP","0"])+"\n"
				if cmdchar=="3":
					gender = gender+[0]
					indic = indic + [2]
					matches=",".join([lowfname,"ABBR","0"])+"\n"
				if cmdchar=="5":
					gender = gender+[1]
					indic = indic + [4]
					matches=",".join([lowfname,lowfname,"1"])+"\n"
					malenames=malenames+[lowfname]
				if cmdchar=="6":
					gender = gender+[2]
					indic = indic + [4]
					matches=",".join([lowfname,lowfname,"2"])+"\n"
					femnames=femnames+[lowfname]
				
				proba = codecs.open("nameclean_comms.txt","a",encoding='utf-8', errors='replace')		
				proba.write(matches)
				proba.close()
			else:
				if processedgender[processednames.index(lowfname)]=="0":
					gender = gender + [0]
					if processedcomms[processednames.index(lowfname)]=="ABBR":
						indic = indic + [2]
					elif processedcomms[processednames.index(lowfname)]=="SKIP":
						indic = indic + [0]
				if processedgender[processednames.index(lowfname)]=="1":
					gender = gender + [1]
					if processedcomms[processednames.index(lowfname)] in malenames_orig:
						indic = indic + [3]
					else:
						indic = indic + [4]
				if processedgender[processednames.index(lowfname)]=="2":
					gender = gender + [2]
					if processedcomms[processednames.index(lowfname)] in femnames_orig:
						indic = indic + [3]
					else:
						indic = indic + [4]
			#CHECK
		

	
	print "****"
	#print malenames
	#print femnames


	# ITT A HIBA, SZAR DOLGOT IROK A FILE/BA NEM A RENDES ID/t
	for i in range(len(malenames)):
		namedict[malenames[i]]=[malenames[i],"1",malenames_ind[i]]

	for i in range(len(femnames)):
		namedict[femnames[i]]=[femnames[i],"2",femnames_ind[i]]

	

	for i in range(len(processednames)):
		finalid=""
		if processedcomms[i] in malenames:
			finalid=str(malenames_ind[malenames.index(processedcomms[i])])
		elif processedcomms[i] in femnames:
			finalid=str(femnames_ind[femnames.index(processedcomms[i])])
		#elif processedcomms[i]==processednames[i]:
			#addednames=addednames+1
			#finalid=str(addednames)	

		namedict[processednames[i]]=[processedcomms[i],processedgender[i],finalid]

	print len(allnames),len(indic),len(gender)
	#print indic
	for i in range(len(allnames)):
		
		if allnames[i] not in namedict:

			if indic[i]==0:
				
				namedict[allnames[i]]=["SKIP","0","0"]
			if indic[i]==2:
				if gender[i]==0:					
					if allnames[i][:-1] not in namedict:
						namedict[allnames[i][:-1]]=["ABBR","0","0"]
				elif gender[i]==2:
					if allnames[i][:-2] in namedict:
						namedict[allnames[i]]=[allnames[i][:-2],"2",namedict[allnames[i][:-2]][2]]
						
					else:
						namedict[allnames[i][:-1]]=["ABBR","2","0"]
						

	json.dump(namedict, codecs.open("name_dict.txt",'w', encoding='utf-8', errors='replace'))		

	return namedict
		#assert len(indic) = len(gender)


			#comp=difflib.SequenceMatcher(None,prev_name,freshname)
			#	if (comp.ratio()<0.3 or prev_name[0]!=freshname[0] or (len(name_elements)==1 and nameline==0)) and nameIsFresh==1:





	# 2. oszd ki a NEM ROVIDITES hibakat
	# 3. csinalj freqdistet
	# 4. oldd fel a roviditeseket

def clean_firstnames(inFileName):
	#inFileName="BPLAKCIMJEGYZEK_10_1898_lakjegyzek_temp_adr.txt"
	outFileName=inFileName.split(".")[0]+"_adr.txt"
		
	freqdistrawfile=inFileName.split(".")[0]+"names_fdist_raw.txt"
	freqdistfile=inFileName.split(".")[0]+"freqdist.txt"
	firstNameWhitelist="firstname_whitelist_withids.txt"

	afterWhichColoumn=2


	namedict = fname_dict_create(inFileName, firstNameWhitelist)

	inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')

	rawnames = []
	for line in inFile:
		name=line.split(",")[1]
		nameels=name.split()
		for j in range(len(nameels)):
			if j>0:
				rawnames=rawnames+[nameels[j]]

	fdfile= codecs.open(freqdistrawfile, "w", encoding="utf-8", errors="replace")
	fdfile.write(",".join(rawnames))
	fdfile.close()
	inFile.close()

	[freq,fdist]=dict_freqdist(namedict,freqdistrawfile)

	fds = codecs.open(freqdistfile, "w", encoding="utf-8", errors="replace")
	for i in range(len(freq)):
		fds.write(freq[i]+","+str(fdist[i])+"\n")



	inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')
	outFile = codecs.open(outFileName,'w', encoding='utf-8', errors='replace')
	outFile.write("ID,name,name1id,name2id,name1,name1gend,name2,name2gend\n")

	for line in inFile:
		ids=name=line.split(",")[0]
		
		name=line.split(",")[1]
		#print name.encode('utf-8')
		nameels=name.split()
		namewhite1=" "
		namewhite2=" "
		namegen1="0"
		namegen2="0"
		gender_override="0"
		nameid1="0"
		nameid2="0"
		if len(nameels)>1:
			[check1,gender_override]=name_preprocess((kill_accents(nameels[1])))
			#print check1		
			if check1 in namedict:

				#print check1,namedict[check1][0],namedict[check1][1]
				namewhite1=namedict[check1][0]
				namegen1=namedict[check1][1]
				nameid1=namedict[check1][2]
				if gender_override=="2":
					namegen1="2"

				if namedict[check1][0]=="ABBR":
					#print "Ragyogok"
					
					namewhite1=lookup_best(check1,freq,fdist)

					if namewhite1=="SKIP":
						namegen1="0"
						nameid1="0"
					else:
						namegen1=namedict[namewhite1][1]
						nameid1=namedict[namewhite1][2]



		if len(nameels)>2:
			#check1=unikill(kill_accents(nameels[2]))
			[check1,gender_override]=name_preprocess((kill_accents(nameels[2])))
			if check1 in namedict:
				namewhite2=namedict[check1][0]
				namegen2=namedict[check1][1]
				nameid2=namedict[check1][2]
				if gender_override=="2":
					namegen2="2"

				if namedict[check1][0]=="ABBR":
					#[freq,fdist]=dict_freqdist(namedict,toclean)
					namewhite2=lookup_best(check1,freq,fdist)
					if namewhite2=="SKIP":
						namegen2="0"
						nameid2="0"
					else:
						namegen2=namedict[namewhite2][1]
						nameid2=namedict[namewhite2][2]

		lineels=line.split(',')
		outline=[kill_accents(name),str(nameid1),str(nameid2),namewhite1,namegen1,namewhite2,namegen2]
		outline=[lineels[0]]+outline
		try:
			#outFile.write(unikill(",".join(outline).encode('utf-8'))+"\n")
			outFile.write(",".join(outline).decode('utf-8')+"\n")
		except:
			outFile.write("unicode error\n")

