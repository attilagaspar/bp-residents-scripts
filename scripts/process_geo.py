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
#from fuzzywuzzy import fuzz
import operator
import msvcrt
import json


from process_basics import *

#########################
# PART 1
# AUXILIARY FUNCTIONS FOR CLEANING THE ADDRESS PART OF THE DATA
#########################


def number_lookup(inList):
	#numbers in addresses often come in pairs (i.e. Baker Street 7-9). This function takes a string (which is supposedly an address) and returns
	#one or two numbers embedded within it

	number=""
	number2=""
	for i in range(len(inList)):
		if contains_digits(inList[i]):
			number = filter(str.isdigit, inList[i].encode('utf-8'))
			number2=""
			# ez itt csak a szamok szurese
			if unicode(str(number)) not in inList[i]:
				
				numbers=[]
				for y in range(len(inList[i].split())):
					if contains_digits(inList[i].split()[y]):
						#delimiters = [" és ".decode('utf-8'),"/","—".decode('utf-8')]
						#for yy in range(len(delimiters)):
						#	for z in range(len(original_name.split()[y].split(delimiters[yy]))):
						#		if contains_digits(original_name.split()[y].split(delimiters[yy])[z]):
						#			numbers=numbers+[original_name.split()[y].split(delimiters[yy])[z]]							

						if "/" in inList[i]:
							for z in range(len(inList[i].split()[y].split("/"))):
								if contains_digits(inList[i].split()[y].split("/")[z]):
									numbers=numbers+[inList[i].split()[y].split("/")[z]]							
						#if "—".decode('utf-8') in numbers[0]:
						#	numbers=[]
						if "—".decode('utf-8') in inList[i]:
							for z in range(len(inList[i].split()[y].split("—".decode('utf-8')))):
								if contains_digits(inList[i].split()[y].split("—".decode('utf-8'))[z]):
									numbers=numbers+[inList[i].split()[y].split("—".decode('utf-8'))[z]]
						if "-".decode('utf-8') in inList[i]:
							for z in range(len(inList[i].split()[y].split("-".decode('utf-8')))):
								if contains_digits(inList[i].split()[y].split("-".decode('utf-8'))[z]):
									numbers=numbers+[inList[i].split()[y].split("-".decode('utf-8'))[z]]
						#for z in range range(len(original_name.split()[y].split(""))):
						#	if contains_digits(original_name.split()[y].split("/")[z]):
						#		numbers=numbers+[original_name.split()[y].split("/")[z]]		
				if len(numbers)>1:
					number=numbers[0].encode('utf-8')
					number2=numbers[1].encode('utf-8')
					number2=number2.split('\n')[0]

	return [number,number2]


def return_command_set_item(relevantLineElements):
	for y in range(len(relevantLineElements)):
		cand =  relevantLineElements[y]
		if contains_digits(cand):
			return strip_number(cand)
	return ""



def check_if_place(inString):
    
	#This function checks if a string contains an address. This done by looking for type markers of public premises (e.g. "Square", "Street") and 
	#their known OCR deformations

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

	#szentkiralyi utcat nem talalja

	foundvalue=-1
	retstring=u""
	stop = 0

	if len(inString)>5:
		for i in range(len(space_dict)):
			for j in range(len(space_dict[i])):
				toCut=len(space_dict[i][j])
				if toCut<len(inString) and stop==0:
					cutString=inString[0:(-toCut)]
					if cutString[-1]==u" " or cutString[-1]==u"-":
						pass
					else:
						suffix=inString[-toCut:]
						#print inString.encode('utf-8')+"    "+cutString.encode('utf-8')+"    "+suffix.encode('utf-8')+"    "+space_dict[i][j].encode('utf-8')
						#print "x"+inString[-len(space_dict[i][j])-1:-1].encode('utf-8') + "x"+"       " + "x"+space_dict[i][j].encode('utf-8')+ "x"
						if suffix==space_dict[i][j]:						
							foundvalue=i
							#print foundvalue
							retstring=cutString
							#print "itt vagyok ragyogok" +"    "+ retstring.encode('utf-8')+"    "+str(i)
							stop=1
						

			if foundvalue==-1:
				for j in range(-len(space_errors[i])):
					toCut=len(space_errors[i][j])
					if toCut<len(inString) and stop==0:
						cutString=inString[0:(-toCut)]
						suffix=inString[-toCut:]
						#print inString.encode('utf-8')+"    "+cutString.encode('utf-8')+"    "+suffix.encode('utf-8')+"    "+space_dict[i][j].encode('utf-8')
						if suffix==space_errors[i][j]:
							foundvalue=i
							retstring=cutString
							#print "itt vagyok ragyogok" +"    "+ retstring.encode('utf-8')+"    "+str(i)
							stop=1
	#print foundvalue				
	#print retstring.encode('utf-8')
	if foundvalue==-1:
		#print "lololo" + retstring.encode('utf-8')
		return [-1,""]
	else:
		#print str(foundvalue+1)+retstring.encode('utf-8')
		return [foundvalue+1,retstring]
		

def check_if_it_was_found_before(filename,comid):
	commandfile = codecs.open(filename,'r', encoding='utf-8', errors='replace')
	found=0
	for i in commandfile:
		if i.split(',')[0]==comid:
			found=1
	if found==1:
		return True
	else:
		return False


def search_for_address_by_code(adrlist,what):

	#this function looks up a place in the address whitelist BY ITS CODE

	listFile = codecs.open(adrlist,'r', encoding='utf-8', errors='replace')
	allstreets = listFile.readlines()
	found=0
	for i in range(len(allstreets)):
		if found==0:
			if allstreets[i].split(',')[0]==str(what):
				ids=allstreets[i].split(',')[0]
				stubs=allstreets[i].split(',')[1]
				types=allstreets[i].split(',')[2]
				fulls=allstreets[i].split(',')[3]
				distrs1=allstreets[i].split(',')[4]
				distrs2=allstreets[i].split(',')[5]
				
				found=1

	listFile.close()
	alldata=[]
	if found==1:
		retstring=",".join([ids,stubs,types,fulls,distrs1,distrs2])
		return retstring
	else:
		return ""


	#alldata=sorted(zip(qual,ids,stubs,types,fulls,distrs1,distrs2).iteritems(), key=operator.itemgetter(0))[0:4]
	return alldata

def search_for_address(adrlist,what):

	#this function looks up a place in the address whitelist BY ITS NAME

	listFile = codecs.open(adrlist,'r', encoding='utf-8', errors='replace')
	allstreets = listFile.readlines()
	ids=[]
	stubs=[]
	inos=[]
	types=[]
	fulls=[]
	distrs1=[]
	distrs2=[]


	for i in range(len(allstreets)):
		if what in allstreets[i].split(',')[3].lower():
			ids=ids+[allstreets[i].split(',')[0]]
			stubs=stubs+[allstreets[i].split(',')[1]]
			types=types+[allstreets[i].split(',')[2]]
			fulls=fulls+[allstreets[i].split(',')[3]]
			distrs1=distrs1+[allstreets[i].split(',')[4]]
			distrs2=distrs1+[allstreets[i].split(',')[5]]
			inos=inos+[str(i)]

	alldata=[]
	listFile.close()
	for i in range(len(ids)):
		alldata=alldata+[[inos[i],ids[i],stubs[i],types[i],fulls[i],distrs1[i],distrs2[i]]]


	#alldata=sorted(zip(qual,ids,stubs,types,fulls,distrs1,distrs2).iteritems(), key=operator.itemgetter(0))[0:4]
	return alldata

#########
# PART 2
# THE MAIN FUNCTION CLEANING ADDRESSES
#########



def match_with_address_list(inFileName, listFileName, outFileName, readlog, autoPilotStartsAt=-1, readingStartsAt=-1):
	#this function pairs lines with addresses. 
	
	#inFileName: source file
	#listFileName: whitelist file
	#outFileName: destination file
	#readLog: name of command file
	#autoPilotStartsAt: line number from which the program does not ask for further inputs just performs operations it has learned or skips the line altogether
	#readingStartsAt: if you want to start from not the first line but later ones

	#informative part starts at
	geodata_starts=10
	#number of uninformative coloumns in the back
	uninformative=2

	# required match quality
	eps = 0.74
	# ebbol lesz a foglalkozas whitelist
	lastcmnfile = codecs.open('lastrow.txt','w', encoding='utf-8', errors='replace')
	inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')
	outFile = codecs.open(outFileName,'w', encoding='utf-8', errors='replace')
	failName = outFileName[0:-4]+"_fail.txt"
	failFile = codecs.open(failName,'w', encoding='utf-8', errors='replace')
	failFile.write("This file reports matching failures.\n")
	failFile.close()

	clFileName = "address_cleaning_log.txt"
	try:
		clFile=codecs.open(clFileName, 'r', encoding='utf-8', errors='replace')
		clFile.close()
	except:
		clFile=codecs.open(clFileName, 'w', encoding='utf-8', errors='replace')
		clFile.close()

	
	# handling autopilot: 
	if autoPilotStartsAt>-1:
		clFileName2="address_cleaning_log"+str(autoPilotStartsAt)+".txt"
		clFile2=codecs.open(clFileName2, 'w', encoding='utf-8', errors='replace')
		clFile=codecs.open(clFileName, 'r', encoding='utf-8', errors='replace')
		for lines in clFile:
			clFile2.write(lines)
		clFile.close()
		clFile2.close()
	else:
		clFileName2=clFileName

	
	upName=listFileName[0:-9]+"_ujpest.txt"
	budName=listFileName


	#### AUTOPILOT
	#### if this is set to 1, the code skips any line in the data which would need human interaction. 

	autopilot = 0

	#####################  XI. 21: I add this part
	###### whenever one makes any choice or reads one  from the log, the choice he makes is put into a dictionary
	###### it should be checked first whether the same decision had been made before and if so it should be done again
	###### choice_dict: ["string" : code]
	choice_dict={}
	
#	try:
	line=0
	ujpest=0
	type_aut1=0
	type_aut2=0
	type_aut3=0
	type_cod=0
	type_inp=0
	type_saut=0
	type_patt=0
	print autoPilotStartsAt
	for lines in inFile:

		#print "\n"
		#print lines.encode('utf-8')

		command_read_from_file=0
		cmd_index=0
		skipped_line=0
		address_is_in=11

		line=line+1
		#if line%1000==0:
		#	print line
		lineElements=lines.split(",")
		id = lineElements[0].rstrip("\n")

		#HERE YOU CAN TELL WHERE THE PROGRAM STARTS FROM
		
		readingStartsAt=0

		if contains_digits(id) and int(id)>readingStartsAt:

			if int(id)>autoPilotStartsAt and autoPilotStartsAt!=-1:
				autopilot=1
			if int(id) % 50 == 0:
				os.system('cls')
				print "current:",str(id),",aut1:",type_aut1,",aut2:",type_aut2,",aut3:",type_aut3,",saut:",type_saut,",cod:",type_cod,",inp:",type_inp,",pat:",type_patt,"/",len(choice_dict)

			if len(choice_dict) % 10 == 0:
				json.dump(choice_dict, codecs.open("temp_dict.txt",'w', encoding='utf-8', errors='replace'))

			# DECIDE WHICH WL TO USE / ARE WE IN UJPEST?
			ujpest=0
			if u"Újpest"  in lines:
				#raw_input(lines.encode('utf-8'))
				#or u"ujpesti" or u"újpesti"
				ujpest=1
			if ujpest==1:
				listFileName=upName
			if ujpest==0:
				listFileName=budName


			#szarokat ki kell dobni
			for zz in range(uninformative):
				del(lineElements[-1])


			matches = 0
			wrongnumber=u"#ok"
			match_list=[]
			d1=[]
			d2=[]
			match_id=[]
			match_full=[]
			matched_with=[]
			match_quality=[]
			match_type=[]
			#	comp=difflib.SequenceMatcher(None,prev_name,freshname)
			#	if (comp.ratio()<0.3 or prev_name[0]!=freshname[0] or (len(name_elements)==1 and nameline==0)) and nameIsFresh==1:


			final_name=u"NO MATCH"
			final_id=u"NO MATCH"
			final_full=u"NO MATCH"
			final_type=u"FAIL"
			original_name="none"
			final_d1="0"
			final_d2="0"
			final_found=0

			
			##################################################################################################
			# CLEANING TIER 1
			# pontos matchek es statisztikailag nagyon jo matchek (quality>eps)
			##################################################################################################
			#sorry
			if 5==5:
			
				for x in range(geodata_starts,len(lineElements)):

					# this variable tells whether the streetname string is found in the dictionary of past choices
					found_in_dict=0
		
					candidate=lineElements[x]
					stringToCheck=strip_number(candidate)

					[placeType,nameStub]=check_if_place(stringToCheck)
					#########################################
					# ez fontos lehet, ha keveset talal meg
					# if nameStub=="": nameStub==stingToCheck
					#########################################
					if placeType!=-1:
						listFile = codecs.open(listFileName,'r', encoding='utf-8', errors='replace')
						for toMatch in listFile:			
							toMatchElems=toMatch.split(",")
							streetID=toMatchElems[0]
							streetName=toMatchElems[1]
							streetTypeWhite=int(toMatchElems[2])
							streetFullName=toMatchElems[3]
							distr1=toMatchElems[-4]
							distr2=toMatchElems[-3]
							#egymast tartalmazo stringek dummyija
							danger1=int(toMatchElems[-2])
							danger2=int(toMatchElems[-1])
							streetName2=streetName.lower()

							#print str(placeType) + "    " + str(streetTypeWhite)
							if placeType==streetTypeWhite:
								#print "itt vagyok ragyogok"
								#esetek
								#1: tökéletes match
								#2: fuzzy, azonos hosszúság
								#3: setes fuzzy, de buntetni kell a hosszusag kulonbseget (50% = -100 pont)
								if nameStub==streetName or nameStub==streetName2:
									match_quality=match_quality+[5]
									match_list=match_list+[streetName]
									match_id=match_id+[streetID]
									match_full=match_full+[streetFullName]
									matched_with=matched_with+[candidate]
									d1=d1+[distr1]
									d2=d2+[distr2]
									matches=matches+1
									match_type=match_type+["aut1"]

								elif len(nameStub)==len(streetName):
									#match_quality=match_quality+[fuzz.token_set_ratio(nameStub.lower,streetName2)]
									comp=difflib.SequenceMatcher(None,nameStub.lower(),streetName2)
									qual=comp.ratio()
									match_quality=match_quality+[qual]
									match_list=match_list+[streetName]
									match_id=match_id+[streetID]
									match_full=match_full+[streetFullName]
									matched_with=matched_with+[candidate]
									d1=d1+[distr1]
									d2=d2+[distr2]
									matches=matches+1
									match_type=match_type+["aut2"]

								else:
									comp=difflib.SequenceMatcher(None,nameStub.lower(),streetName2)
									qual=comp.ratio()
							
									x1=len(nameStub)
									x2=len(streetName2)
									aa=x1/x2
									bb=x2/x1
									sizediff=min([aa, bb])
									#if sizediff>2:
									#	q=0
									#else:
									#	q=q-100*(sizediff-1)

									#match_quality=match_quality+[qual*sizediff]
									match_quality=match_quality+[qual]

									match_list=match_list+[streetName]
									match_id=match_id+[streetID]
									match_full=match_full+[streetFullName]
									matched_with=matched_with+[candidate]
									d1=d1+[distr1]
									d2=d2+[distr2]
									matches=matches+1
									match_type=match_type+["aut3"]

						listFile.close()
				# ha az eddigi nem volt sikeres, csinalunk egy ujat, de durvan meg lesz penalizalva
				# fuzzy matches



				

			if matches>1:
				#print "\n"
				#print lines.encode('utf-8')+"\n"
				#for i in range(len(match_list)):
				#	print str(i) + " " +match_id[i].encode('utf-8')+" "+ match_full[i].encode('utf-8')+ " " + matched_with[i].encode('utf-8') + " " + str(match_quality[i]-match_quality[i]%0.001)
				#answer=input()
				#if not answer:
				answer = match_quality.index(max(match_quality))
				#print "\n"
				#rint 
				#print answer, len(match_list)
				final_quality=match_quality[int(answer)]
				if final_quality>eps:
					final_name=match_list[int(answer)]
					final_type=str(match_type[int(answer)])
					
					#keep track of how many matching types are there
					if final_type=="aut1":
						type_aut1=type_aut1+1
					if final_type=="aut2":
						type_aut2=type_aut2+1
					if final_type=="aut3":
						type_aut3=type_aut3+1

					final_id=match_id[int(answer)]
					final_full=match_full[answer]
					final_d1=d1[answer]
					final_d2=d2[answer]
					original_name=matched_with[answer]
					final_found=1
			elif matches==1:
				final_quality=match_quality[0]
				if final_quality>eps:
					final_name=match_list[0]
					final_id=match_id[0]
					final_full=match_full[0]
					final_type=str(match_type[0])
					
					#keep track of how many matching types are there
					if final_type=="aut1":
						type_aut1=type_aut1+1
					if final_type=="aut2":
						type_aut2=type_aut2+1
					if final_type=="aut3":
						type_aut3=type_aut3+1

					final_quality=match_quality[0]
					final_d1=d1[0]
					final_d2=d2[0]
					original_name=matched_with[0]
					final_found=1


			################################################
			#tier2
			#if eps is not small enough, give them by hand
			################################################
			
			#noac: number of answer candidates: the length of the list or 3, whichever is smaller

			
			# FIRST LET'S SEE IF A CHOICE WAS GIVEN PREVIOUSLY
			if final_found==0:
				clFile=codecs.open(clFileName, "r", encoding="utf-8", errors="replace")
				for cmdlines in clFile:
					cmdlines=cmdlines.split("\n")[0]
					comid = cmdlines.split(",")[1]
					comm = cmdlines.split(",")[0]
					#print comid,id,int(comid)
					#print comm
					if int(comid) == int(id):
						
						if comm=="input":
							strid = cmdlines.split(",")[3]
							comaddr = cmdlines.split(",")[4]
							listFile = codecs.open(listFileName,'r', encoding='utf-8', errors='replace')
							for toMatch in listFile:
					
								toMatchElems=toMatch.split(",")
								if int(strid)==int(toMatchElems[0]):
									final_name=toMatchElems[1]
									final_id=strid
									final_full=toMatchElems[3]
									
									final_quality="man"
									final_type="inp"
									type_inp=type_inp+1
									final_d1=toMatchElems[4]
									final_d2=toMatchElems[5]
									original_name=cmdlines.split(",")[1]
									number=cmdlines.split(",")[-2]
									number2=cmdlines.split(",")[-1]
									wrongnumber="man"
									final_found=1
									command_read_from_file=1
									# if line is short this might fail
									learnable_pattern=return_command_set_item(lineElements[9:])
									if learnable_pattern!="":
										if learnable_pattern not in choice_dict:
											choice_dict[learnable_pattern]=strid



							listFile.close()
						if comm=="codeinput":
							commadr=int(cmdlines.split(",")[3])
							if commadr>1999 and commadr<3000:
								adrlist=upName
							else:
								adrlist=budName	
							streetFoundByCode=search_for_address_by_code(adrlist,commadr)
							#print "found ",streetFoundByCode.encode("utf-8")
							if streetFoundByCode!="":
								retr_data=streetFoundByCode.split(",")
									#retstring=",".join(ids,stubs,types,fulls,distrs1,distrs2)
									
								final_name=retr_data[1]
								final_id=retr_data[0]
								final_full=retr_data[3]
								
								final_quality="man"
								final_d1=retr_data[4]
								final_d2=retr_data[5]
								final_type="cod"
								type_cod=type_cod+1
								number=cmdlines.split(",")[-2]
								number2=cmdlines.split(",")[-1]
								wrongnumber="man"
								original_name="codegiven"							
								final_found=1
								command_read_from_file=1
								#if line is short this might fail
								learnable_pattern=return_command_set_item(lineElements[9:])
								if learnable_pattern!="":
									if learnable_pattern not in choice_dict:
										choice_dict[learnable_pattern]=str(final_id)
								
						if comm=="choice":
							#choice,206,205,no1,no2
							strid = cmdlines.split(",")[2]
							number=cmdlines.split(",")[3]
							number2=cmdlines.split(",")[4]
							listFile = codecs.open(listFileName,'r', encoding='utf-8', errors='replace')
							for toMatch in listFile:				
								toMatchElems=toMatch.split(",")
								if int(strid)==int(toMatchElems[0]):
									final_name=toMatchElems[1]
									final_id=strid
									final_full=toMatchElems[3]							
									final_quality="man"
									final_type="saut"
									type_inp=type_inp+1
									final_d1=toMatchElems[4]
									final_d2=toMatchElems[5]
									original_name="saut_choice"
									wrongnumber="man"
									final_found=1
									command_read_from_file=1
									#if line is short this might fail
									learnable_pattern=return_command_set_item(lineElements[9:])
									if learnable_pattern!="":
										if learnable_pattern not in choice_dict:
											choice_dict[learnable_pattern]=str(final_id)
							listFile.close()

						if comm=="skip":
							final_found=1
							skipped_line=1
							nal_type="FAIL"


				clFile.close()
			
			# LET'S SEE IF THERE IS A PATTERN WE HAVE LEARNED PREVIOUSLY WHILE THE SCRIPT WAS RUNNING
			if final_found==0:
				
				
				found_pattern=return_command_set_item(lineElements[geodata_starts:])
				if found_pattern!="":
					if found_pattern in choice_dict:
						print lines.encode('utf-8')
						clFile=codecs.open(clFileName2, "a", encoding="utf-8", errors="replace")
						final_id=choice_dict[found_pattern]				
						commadr=int(final_id)
						if commadr>1999 and commadr<3000:
								adrlist=upName
						else:
								adrlist=budName	
						streetFoundByCode=search_for_address_by_code(adrlist,commadr)
						retr_data=streetFoundByCode.split(",")
						final_name=retr_data[1]
						final_full=retr_data[3]
						final_quality="man"
						final_d1=retr_data[4]
						final_d2=retr_data[5]
						final_type="pat"
						type_patt=type_patt+1
						command_read_from_file=1
						
						number=cmdlines.split(",")[-2]
						number2=cmdlines.split(",")[-1]
						print "pattern found for ", final_name.encode('utf-8')
						[number1def,number2def]=number_lookup(lineElements[geodata_starts:])
						
						if not check_if_it_was_found_before(clFileName2,str(id)):
							if autopilot==0:
								if number1def=="":
									number=raw_input("give numbers manually, number1: %s"%number1def + chr(8)*len(number1def))
									if not number:
										number=number1def									
										print "\n"
									number2=raw_input("number2: %s"%number2def + chr(8)*len(number2def))
									if not number2:
										number2=number2def									
										print "\n"

									commandline = "pattern,"+str(id)+","+found_pattern+","+final_id+","+final_name+","+number+","+number2+"\n"
									clFile.write(commandline)
								else:
									number=number1def
									number2=number2def
							else:
								number=number1def
								number2=number2def
								# SOME UNICODE CHARACTERS ARE HOPELESS
								try:
									commandline = "pattern,"+str(id)+","+found_pattern.encode('utf-8')+","+final_id.encode('utf-8')+","+final_name.encode('utf-8')+","+number.encode('utf-8')+","+number2.encode('utf-8')+"\n"
									clFile.write(commandline.encode('utf-8'))
								except: 
									commandline="pattern,"+str(id)+","+"could not decode some characters"+final_id.encode('utf-8')+"\n"
									clFile.write(commandline.encode('utf-8'))
						
						wrongnumber="man"
						original_name="codegiven"
						
						clFile.close()


						final_found=1
						ff=1
					
			##############################################################
			############ STARTING FROM HERE THIS IS OFF IF AUTOPILOT IS ON
			##############################################################

			if autopilot==0:

				if final_found==0:
					clFile=codecs.open(clFileName2, "a", encoding="utf-8", errors="replace")
					print "\n"
					noac = min([3,len(match_list)])
					print len(match_list)
					
					if noac>0:
						
						#noac=2
						#print len(match_quality)
						#print len(match_list)
						#print len(match_id)
						#print len(match_full)
						#print len(matched_with)
						#print len(match_type)
						#print len(d1)
						#print len(d2)

						sorted_name = []
						sorted_type = []
						sorted_id = []
						sorted_full = []
						sorted_d1 = []
						sorted_d2 = []
						sorted_orig = []
						sorted_quality=[]

						for i in range(noac):
							biggest = match_quality.index(max(match_quality))
							sorted_name = sorted_name+[match_list.pop(biggest)]
							sorted_type = sorted_type+[match_type.pop(biggest)]
							sorted_id = sorted_id+[match_id.pop(biggest)]
							sorted_full = sorted_full+[match_full.pop(biggest)]
							sorted_d1 = sorted_d1+[d1.pop(biggest)]
							sorted_d2 = sorted_d2+[d2.pop(biggest)]
							sorted_orig = sorted_orig+[matched_with.pop(biggest)]
							sorted_quality = sorted_quality+[match_quality.pop(biggest)]

						#print len(sorted_name), sorted_name
						#print len(sorted_type), sorted_type
						#print len(sorted_id), sorted_id
						#print len(sorted_full), sorted_full
						#print len(sorted_d1), sorted_d1
						#print len(sorted_d2), sorted_d2
						#print len(sorted_orig), sorted_orig
						#print len(sorted_quality), sorted_quality

						#print "\n"	
						print lines.encode('utf-8')
						
						print "no match found automatically. please choose one from the list below or press any other key to override"
						for i in range(noac):
							print "\n"
							print "press  " + str(i) + "  to choose the following:"
							print sorted_id[i].encode("utf-8"),sorted_orig[i].encode("utf-8"),sorted_full[i].encode("utf-8")
							print sorted_d1[i]+" " +sorted_d2[i]

						cmdchar = msvcrt.getch()
						
						if cmdchar.isdigit():
							if int(cmdchar)<noac:
								choice=int(cmdchar)
								final_name=sorted_name[choice]
								final_id=sorted_id[choice]
								final_full=sorted_full[choice]
								final_type="4"
								final_quality=sorted_quality[choice]
								final_d1=sorted_d1[choice]
								final_d2=sorted_d2[choice]
								original_name=sorted_orig[choice]
								final_found=1
								final_type="saut"
								cmd_index=sorted_id[choice]
								

					##############################################################
					# TIER 3 
					# ask name to look up in dictionary
					##############################################################
					if final_found==0:
						ff=0
						while ff==0:
							
						
							print id,lines.encode('utf-8')
							what=raw_input("give a string/give a WL code/press x to skip line/n to add a new address:\n")
							
							if what!="x":
								if is_number(what):
									print "looking up code", what
									street_code=int(what)
									if street_code>1999 and street_code<3000:
										adrlist=upName
									else:
										adrlist=budName								
									streetFoundByCode=search_for_address_by_code(adrlist,street_code)
									print "found ",streetFoundByCode.encode("utf-8")
									if streetFoundByCode!="":
										retr_data=streetFoundByCode.split(",")
										#retstring=",".join(ids,stubs,types,fulls,distrs1,distrs2)
										
										final_name=retr_data[1]
										final_id=retr_data[0]
										final_full=retr_data[3]								
										final_quality="man"
										final_d1=retr_data[4]
										final_d2=retr_data[5]

										#Kisegitjuk a felhasznalot azzal, hogy kikeressuk elore a szamkodokat
										#for x in range(9,len(lineElements)):

										[number1def,number2def]=number_lookup(lineElements[9:])
										number=raw_input("give numbers manually, number1: %s"%number1def + chr(8)*len(number1def))
										if not number:
											number=number1def									
										print "\n"
										number2=raw_input("number2: %s"%number2def + chr(8)*len(number2def))
										if not number2:
											number2=number2def									
										print "\n"

										original_name="codegiven"
										wrongnumber="man"
										commandline = "codeinput,"+str(id)+","+what+","+final_id+","+final_name+","+number+","+number2+"\n"
										clFile.write(commandline)
										final_found=1
										ff=1
										final_type="cod"
										type_cod=type_cod+1

										learnable_pattern=return_command_set_item(lineElements[geodata_starts:])
										if learnable_pattern!="":
											if learnable_pattern not in choice_dict:
												choice_dict[learnable_pattern]=str(what)


								else:
									if what=="n":
										# HERE COMES CODE FOR NEW RECORD
										# identify number
										lastitemid=0
										adrlist1=codecs.open(listFileName, "r", encoding="utf-8", errors="replace")
										addresses=adrlist1.readlines()
										for items in range(1,len(addresses)):
											checkadrid = int(addresses[items].split(",")[0])
											if lastitemid<checkadrid:
												lastitemid=checkadrid
										adrlist1.close()
										itemid=lastitemid+1

										# give name
										newname=raw_input("name of new object:")
										newtype=raw_input("type of new object:")
										
										# give numbers
										newdistrict1=raw_input("district1:")
										newdistrict2=raw_input("district2:")
										adrline=",".join([str(itemid),newname,newtype,newname,newdistrict1,newdistrict2,"0","0"])+"\n"
										adrlist1=codecs.open(listFileName, "a", encoding="utf-8", errors="replace")
										adrlist1.write(adrline)
										adrlist1.close()


										[number1def,number2def]=number_lookup(lineElements[geodata_starts:])
										number=raw_input("give numbers manually, number1: %s"%number1def + chr(8)*len(number1def))
										if not number:
											number=number1def									
										print "\n"
										number2=raw_input("number2: %s"%number2def + chr(8)*len(number2def))
										if not number2:
											number2=number2def									
										print "\n"
										

										final_name=newname
										final_id=str(itemid)
										final_full=newname
										final_quality="man"
										final_d1=newdistrict1
										final_d2=newdistrict2

										original_name="manually"
										wrongnumber="man"
										commandline = "codeinput,"+str(id)+","+what+","+final_id+","+final_name+","+number+","+number2+"\n"
										clFile.write(commandline)
										final_found=1
										ff=1
										final_type="cod"
										type_cod=type_cod+1

										learnable_pattern=return_command_set_item(lineElements[geodata_starts:])
										if learnable_pattern!="":
											if learnable_pattern not in choice_dict:
												choice_dict[learnable_pattern]=final_id


									else:
										addresslookup = search_for_address(listFileName,what.rstrip())
										
										print "choose the correct number and press enter\n"
										for i in range(len(addresslookup)):
											print str(i)
											print ",".join(addresslookup[i]).encode('utf-8')
											print "\n"
										cmdchar=msvcrt.getch()
										if cmdchar.isdigit():
											choice=int(cmdchar)
											if choice<len(addresslookup):
												choice=int(cmdchar)
												# kikeressuk a szamkodokat
												[number1def,number2def]=number_lookup(lineElements[geodata_starts:])							
												number=raw_input("give numbers manually, number1: %s"%number1def + chr(8)*len(number1def))
												if not number:
													number=number1def									
												print "\n"
												number2=raw_input("number2: %s"%number2def + chr(8)*len(number2def))
												if not number2:
													number2=number2def									
												print "\n"

												wrongnumber="man"
												final_name=addresslookup[choice][2]
												final_id=addresslookup[choice][1]
												final_full=addresslookup[choice][4]
												final_type="inp"
												type_inp=type_inp+1
												final_quality=addresslookup[choice][0]
												final_d1=addresslookup[choice][5]
												final_d2=addresslookup[choice][6]
												original_name=what
												final_found=1
												ff=1
												commandline = "input,"+str(id)+","+what+","+final_id+","+final_name+","+number+","+number2+"\n"
												clFile.write(commandline)
							else:
								ff=1
								commandline = "skip,"+str(id)+"\n"
								final_type="FAIL"
								clFile.write(commandline)
								skipped_line=1
								clFile.close()
			######### TRIGGER: AUTOPILOT IS ON, NOTHING IS FOUND, PRINT FAILURE
			else:
				if final_found==0:
					ff=1

					commandline = "skip,"+str(id)+"\n"
					final_type="FAIL"
					clFile=codecs.open(clFileName2, "a", encoding="utf-8", errors="replace")
					clFile.write(commandline)
					skipped_line=1
					clFile.close()
			###########################################################
			############ END: OFF IF AUTOPILOT IS ON###################


			# EXTRACTING NUMBERS
			if final_type!="cod" and final_type!="inp" and final_type!="pat":
				number = filter(str.isdigit, original_name.encode('utf-8'))
				number2=""
				# ez itt csak a szamok szurese
				if unicode(str(number)) not in original_name:
					wrongnumber="checknumber"
					numbers=[]
					for y in range(len(original_name.split())):
						if contains_digits(original_name.split()[y]):
							#delimiters = [" és ".decode('utf-8'),"/","—".decode('utf-8')]
							#for yy in range(len(delimiters)):
							#	for z in range(len(original_name.split()[y].split(delimiters[yy]))):
							#		if contains_digits(original_name.split()[y].split(delimiters[yy])[z]):
							#			numbers=numbers+[original_name.split()[y].split(delimiters[yy])[z]]							

							if "/" in original_name:
								for z in range(len(original_name.split()[y].split("/"))):
									if contains_digits(original_name.split()[y].split("/")[z]):
										numbers=numbers+[original_name.split()[y].split("/")[z]]							
							#if "—".decode('utf-8') in numbers[0]:
							#	numbers=[]
							if "—".decode('utf-8') in original_name:
								for z in range(len(original_name.split()[y].split("—".decode('utf-8')))):
									if contains_digits(original_name.split()[y].split("—".decode('utf-8'))[z]):
										numbers=numbers+[original_name.split()[y].split("—".decode('utf-8'))[z]]
							if "-".decode('utf-8') in original_name:
								for z in range(len(original_name.split()[y].split("-".decode('utf-8')))):
									if contains_digits(original_name.split()[y].split("-".decode('utf-8'))[z]):
										numbers=numbers+[original_name.split()[y].split("-".decode('utf-8'))[z]]
							#for z in range range(len(original_name.split()[y].split(""))):
							#	if contains_digits(original_name.split()[y].split("/")[z]):
							#		numbers=numbers+[original_name.split()[y].split("/")[z]]		
					if len(numbers)>1:
						number=numbers[0].encode('utf-8')
						number2=numbers[1].encode('utf-8')
						number2=number2.split('\n')[0]

			#if number=="" or skipped_line==1:
			if final_type=="FAIL":
				number="MISSINGNO"
				failFile = codecs.open(failName,'a', encoding='utf-8', errors='replace')
				failLine=str(id)+','+','.join(lineElements)+"\n"
				failFile.write(failLine)
				failFile.close()

			if number2=="":
				number2="0"

			# MEG KELL KERESNI, MELYIK MEZO A CIM, ES AZT NEM VINNI TOVABB
			keep_address=0
			if number!="MISSINGNO":
				for i in range(len(lineElements)):
					if i>8:
						try:
							if number.encode("utf-8", errors='replace') in lineElements[i].encode("utf-8", errors='replace'):
								address_is_in=i
						except:
							address_is_in=len(lineElements)-1
			address_end=0
			if number2!="0":
				for i in range(len(lineElements)):
					if i>8:
						try:
							if number2 in lineElements[i]:
								occurrences=[m.start() for m in re.finditer(number2, lineElements[i])]	
								pos=occurrences[-1]					
								if len(lineElements[i])-pos>3:
									keep_address=1
						except:
							keep_address=1

			outLine=lineElements[0:geodata_starts-1]+[str(final_quality),final_id,final_name,number.decode('utf-8'),number2.decode('utf-8'),final_d1,final_d2,wrongnumber,final_type,final_full,original_name]		
			if keep_address==0 and address_is_in<len(lineElements):
				
				#outLine=[str(id)]+lineElements[0:9]+[str(final_quality),final_id,final_name,number.decode('utf-8'),number2.decode('utf-8'),final_d1,final_d2,wrongnumber,final_type,final_full,original_name]		
				lineElements.pop(address_is_in)

			outLine=outLine+lineElements[geodata_starts:]

			
			outFile.write(",".join(outLine)+"\n")
			#print ",".join(outLine).encode('utf-8')+"\n"

			if final_type=="saut" and command_read_from_file==0:			
				commandline = u"choice," +unicode(str(id))+","+str(cmd_index).encode("utf-8")+","+number+","+number2+u"\n"
				#print commandline.decode('utf-8')
				#print type(commandline)	
				type_saut=type_saut+1
				clFile=codecs.open(clFileName2, "a", encoding="utf-8", errors="replace")
				clFile.write(commandline.encode("utf-8"))
				clFile.close()
				learnable_pattern=return_command_set_item(lineElements[geodata_starts:])
				if learnable_pattern!="":
					if learnable_pattern not in choice_dict:
						choice_dict[learnable_pattern]=str(final_id)






	return True