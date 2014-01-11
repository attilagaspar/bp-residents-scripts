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
from fuzzywuzzy import fuzz
import operator
import msvcrt
import json

from process_basics import *
from process_geo import *
from process_firstname import *



def read_command_from_KB():
	rawCommand=raw_input("please give a command:")
	rawList=rawCommand.split(" ")
	command = rawList[0]
	argument= " ".join(rawList[1:])
	return [command,argument]

def read_command_from_file(commandImport,cmdNo):
	command=u""
	commandstring=u""
	cmdFile = codecs.open(commandImport,'r', encoding='utf-8', errors='replace')
	for line in cmdFile:
		lineElements=line.split(',')
		if lineElements[0]==str(cmdNo):
			command=lineElements[1]
			commandstring=lineElements[-1]
			print "command read from line "+lineElements[0]
	return [command,commandstring]


def read_process_commands(commandImport):
	returnList=[]	
	cmdFile = codecs.open(commandImport,'r', encoding='utf-8', errors='replace')
	for line in cmdFile:
		line.strip()
		lineElements=line.split(' ')
		command = lineElements[0].rstrip(u'\n')
		argument = u" ".join(lineElements[1:])
		argument.rstrip(u'\n')
		argument=argument.split(u'\n')[0]
		argument=argument.split(u'\r')[0]
		returnList=returnList+[[command,argument]]
	return returnList


def appendCommandFile(commandImport,cmdNo,cmd,cmdStr):
	command=""
	try:
		cmdFile = codecs.open(commandImport,'a', encoding='utf-8', errors='replace')
		cmdFile.write(str(cmdNo)+","+cmd+","+cmdStr+"\n")
		print "command written to file"+"\n"
		return 1
	except:
		print "I/O error"
		return 0



def find_in_database(dbFileName,what,where):
	resultList=[]
	dbFile = codecs.open(dbFileName,'r', encoding='utf-8', errors='replace')
	for lines in dbFile:
		lineElements=lines.split(",")
		if where==-1:
			resultNo=0
			for element in range(len(lineElements)):
				if what in lineElements[element]:
					resultNo=resultNo+1
					if resultNo==1:
						resultList=resultList+[[lines,resultNo]]
					if resultNo>1:
						resultList[-1][1]=resultNo
		if where>-1:
			#print "cig"
			#print lineElements[1]
			if what in lineElements[where]:
				resultList=resultList+[lines]
	return resultList		

def uniHungarian(instring):
	hunChars=['á','é','í','ó','ö','ő','ü','ű','Á','É','Í','Ó','Ö','Ő','Ü','Ű']


def list_coloumn(dbFileName, inArgument):
	col = int(inArgument)
	resultList=[]
	countList=[]
	dbFile = codecs.open(dbFileName,'r', encoding='utf-8', errors='replace')
	for lines in dbFile:
		lineElements=lines.split(",")
		if lineElements[col] in resultList:
			countList[resultList.index(lineElements[col])]=countList[resultList.index(lineElements[col])]+1
			pass
		else:
			resultList.append(lineElements[col])
			countList=countList+[1]
	return [resultList,countList]


def span_DB(dbFileName,outFileName):
	dbFile = codecs.open(dbFileName,'r', encoding='utf-8', errors='replace')
	outFile = codecs.open(outFileName,'w', encoding='utf-8', errors='replace')
	for lines in dbFile:
		lineElements=lines.split(",")
		id = lineElements[-1].rstrip("\n")
		#szarokat ki kell dobni
		del(lineElements[-1])
		del(lineElements[-1])
		del(lineElements[-1])
		del(lineElements[-1])
		name=lineElements[0]
		address=u"N/A"
		district=u"N/A"
		job=u"N/A"
		if len(lineElements)>9:
			if len(lineElements)>12:
				address=lineElements[-1]
				district=lineElements[-2]
				job=" ".join(lineElements[10:-3])
			if len(lineElements)==12:
				address=lineElements[-1]
				district=lineElements[-2]
				job=lineElements[-3]
			if len(lineElements)==11:
				address=lineElements[-1]
				district=lineElements[-2]
			if len(lineElements)==10:
				address=lineElements[-1]
		outFile.write(",".join([id,name,address,district,job,",".join(lineElements[2:9])])+"\n")
	return True
#	except:



def firstname_freqdist(inFileName, colNo):

	########### innen lett kivagva

	eps=0.9
	inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')
	names = []
	accentednames=[]
	re.U
	asszony=0
	for lines in inFile:
		if len(lines.split(",")[colNo].split())>1:
			string = lines.split(",")[colNo].split()[1]
			rxp=re.compile(u"[A-ZÁÉÍÓÖŐÜŰ][a-záéíóöőüú.]*")
			if string[-2:]==u"né" or string[-2:]==u"ne":
				asszony=asszony+1
				string=string[:-3]
				if len(string)>=1 and string[-1]=="-":
					string=string[:-2]
			if rxp.match(string):
				names=names+[killAccents(string).lower()]
				#names=names+[unidecode(string)]
				accentednames=accentednames+[string]

	print len(names)
	print asszony
	namelist=list(set(sorted(names)))
	namelist.sort()

	print len(namelist)
	nl_numbers = [0]*len(namelist)

	for i in range(len(names)):
		nl_numbers[namelist.index(names[i])]=nl_numbers[namelist.index(names[i])]+1

	freqd = zip(namelist, nl_numbers)

	json.dump(dict(freqd), codecs.open("freqdist.txt",'w', encoding='utf-8', errors='replace'))

	outFile = codecs.open("keresztnevek.txt",'w', encoding='utf-8', errors='replace')

	nl=namelist
	outlines=[]
	for elements in namelist:
		if elements[-1]==".":
			ambigs=0
			ambs=[]
			for els in nl:
				if els[-1]!=".":
					if len(els)>len(elements):
						#if els[:len(elements)-2]==elements[:-2]:
						if els[:len(elements)-1]==elements[:-1]:
							ambigs=ambigs+1
							ambs=ambs+[els]
			
			ambs_tuple=[]
			
			for z in range(len(ambs)):
				for x in range(len(namelist)):
					if ambs[z]==namelist[x]:
						ambs_tuple=ambs_tuple+[freqd[x]]
			
			#ambs_tuple2=dict((x,y) for [x,y] in ambs_tuple)

			json.dump(dict(ambs_tuple), codecs.open("ambigs.txt",'w', encoding='utf-8', errors='replace'))

			ambs_sorted=sorted(dict(ambs_tuple).iteritems(), key=operator.itemgetter(1))
			
			ambs_str=[]
			for w in range(len(ambs_sorted)):
				#ambs_str=ambs_str+[unicode(ambs_sorted[w][0]),unicode(ambs_sorted[w][1])]
				ambs_str=ambs_str+[unicode(ambs_sorted[w][0]),unicode(ambs_sorted[w][1])]

			#outFile.write(elements+","+str(freqd[namelist.index(elements)][1])+","+",".join(ambs_str)+"\n")
			if len(ambs_sorted)>2:
				outlines=outlines+[[elements,str(freqd[namelist.index(elements)][1]),ambs_str[-2],ambs_str[-1]]]
			else:
				outlines=outlines+[[elements,str(freqd[namelist.index(elements)][1])]]
		else:
			outlines=outlines+[[elements,str(freqd[namelist.index(elements)][1])]]
			#outFile.write(elements+","+str(freqd[namelist.index(elements)][1])+",0\n")

	
	for x in range(len(outlines)):
		outlines[x].insert(0,str(x))
		if len(outlines[x])>3:
			outlines[x].insert(1,outlines[x][-2])
		else:
			outlines[x].insert(1,outlines[x][1])
		#if x>0:
		#	comp=difflib.SequenceMatcher(None,outlines[x][1],outlines[x-1][1])		
		#	qual=comp.ratio()
		#	if qual>eps and qual<1:
		#		outlines[x][1]=outlines[x-1][1]

	for ls in outlines:
		outFile.write(",".join(ls)+"\n")
	
	############ generating gold standard

	outFile = codecs.open("keresztnevek.txt",'r', encoding='utf-8', errors='replace')
	whitelistexists=0
	try:
		outFile2 = codecs.open("firstname_whitelist.txt",'a', encoding='utf-8', errors='replace')
		whitelistexists=1
	except:
		outFile2 = codecs.open("firstname_whitelist.txt",'w', encoding='utf-8', errors='replace')

	outFile2.close()
	namesprocessed=[]
	outFile2 = codecs.open("firstname_whitelist.txt",'r', encoding='utf-8', errors='replace')
	for i in outFile2:
		namesprocessed=namesprocessed+[i.split(",")[0]]
	outFile2.close()


	firstname_id=1
	to_read=0
	for i in outFile:	
		if i.split(',')[2][-1]!="." and  i.split(',')[2] not in namesprocessed and to_read!=0:
			print i.encode('utf-8')
			print "press 1 for MAN 2 for WOMAN, any other to skip"
			char = msvcrt.getch()
			if char=="1":
				outFile2 = codecs.open("firstname_whitelist.txt",'a', encoding='utf-8', errors='replace')
				outFile2.write(",".join([i.split(",")[2],"1","\n"]))
				outFile2.close()
				firstname_id=firstname_id+1
			if char=="2":
				outFile2 = codecs.open("firstname_whitelist.txt",'a', encoding='utf-8', errors='replace')
				outFile2.write(",".join([i.split(",")[2],"2","\n"]))
				outFile2.close()
				firstname_id=firstname_id+1

		if i.split(',')[2]==namesprocessed[-1]:
			to_read=1
			firstname_id=len(namesprocessed)+1


	#print namelist
	abbrev=[]
	woman=[]


def save_names(dbFileName, colNo, firstNameFile, lastNameFile):
	# van olyan, hogy egy nev rosszul van scannelve es mondjuk Marta helyett M ta van, akkor lehet hogy meg kene nezni hogy osszeragasszuk ezeket a cuccokat

	dbFile = codecs.open(dbFileName,'r', encoding='utf-8', errors='replace')
	tempFileLast=codecs.open('temp1.txt','w', encoding='utf-8', errors='replace')
	tempFileFirst=codecs.open('temp2.txt','w', encoding='utf-8', errors='replace')
	fileLength=0
	for lines in dbFile:
		lineElements=lines.split(",")
		nameRaw = lineElements[colNo]
		nameList=nameRaw.split()
		i=0
		for elements in nameList:
			if i==0:
				tempFileLast.write(elements+"\n")
			else:
				tempFileFirst.write(elements+"\n")
			i=i+1
		fileLength=fileLength+1
	tempFileLast.close()
	tempFileFirst.close()
	dbFile.close()
	fileLast=codecs.open('lastnames.txt','w', encoding='utf-8', errors='replace')
	fileFirst=codecs.open('firstnames.txt','w', encoding='utf-8', errors='replace')
	mrs_fileFirst=codecs.open('mrs_firstnames.txt','w', encoding='utf-8', errors='replace')
	
	# PARSING LAST NAMES
	tempFileLast=codecs.open('temp1.txt','r', encoding='utf-8', errors='replace')	
	resultList=[]
	countList=[]

	progress=1
	for lines in tempFileLast:
		#prInd=progress/fileLength*100
		#if floor(prInd)%5==0:
		#	if floor(prInd)%5>treshold:
		#		treshold=floor(prInd)%5
		#		print str(treshold)+"%\n"

		if progress%1000==0:
			print str(progress)+"\n"

		name=lines.split("\n")[0]
		if name in resultList:
			countList[resultList.index(name)]=countList[resultList.index(name)]+1
		else:
			resultList.append(name)
			countList.append(1)
		progress=progress+1

	for i in range(len(resultList)):
		fileLast.write(resultList[i]+","+str(countList[i])+"\n")

	# PARSING FIRST NAMES
	tempFileFirst=codecs.open('temp2.txt','r', encoding='utf-8', errors='replace')	
	resultList=[]
	countList=[]

	progress=1
	for lines in tempFileFirst:
		#prInd=progress/fileLength*100
		#if floor(prInd)%5==0:
		#	if floor(prInd)%5>treshold:
		#		treshold=floor(prInd)%5
		#		print str(treshold)+"%\n"

		if progress%1000==0:
			print str(progress)+"\n"

		name=lines.split("\n")[0]
		if name in resultList:
			countList[resultList.index(name)]=countList[resultList.index(name)]+1
		else:
			resultList.append(name)
			countList.append(1)
		progress=progress+1
		

	resultSort=[]
	countSort=[0]*len(countList)
	resultSort = sorted(resultList)
	for i in range(len(resultSort)):
		countSort[i] = countList[resultList.index(resultSort[i])]
	for i in range(len(resultList)):
		last2chars = resultSort[i][-2:-1]
		if last2chars in ["né".decode('utf-8'),"ne".decode('utf-8')]:
			mrs_fileFirst.write(resultSort[i]+","+str(countSort[i])+"\n")
		else:			
			fileFirst.write(resultSort[i]+","+str(countSort[i])+"\n")

	return True





def do_command(inputFile,inCommand,inArgument):
# find words and print out to screen
# example: python process.py p Antal -1
	if inCommand == u"f":
		where = -1
		print inCommand.encode('utf-8')
		print inArgument.encode('utf-8')		
		where=int(inArgument.split(" ")[1])
		results=find_in_database(inputFile,inArgument.split(" ")[0],where)
		for elements in results:
			if len(elements)==2:
				print elements[0].encode('utf-8')
			else:
				print elements.encode('utf-8')
# find words and print out to file
# example: python process.py p Antal -1 antal.txt
	if inCommand == u"p":
		where = -1
		print inCommand.encode('utf-8')
		print inArgument.encode('utf-8')
		where=int(inArgument.split(" ")[1])
		outFileName=inArgument.split(" ")[2]
		outFile = codecs.open(outFileName,'w', encoding='utf-8', errors='replace')
		results=find_in_database(inputFile,inArgument.split(" ")[0],where)
		for elements in results:
			if len(elements)==2:
				outFile.write(elements[0])
			else:
				outFile.write(elements)

	#if u"names" in inCommand:
	#	print "PROCESSING NAMES"
	#	firstNameWhiteList("paired_test.txt", 1)

	if inCommand == u"col":
		no=inArgument.split(" ")[0]
		outFileName=inArgument.split(" ")[1]
		outFile = codecs.open(outFileName,'w', encoding='utf-8', errors='replace')
		[results,counts]=list_coloumn(inputFile,no)
		sortRes=sorted(results)
		for x in range(len(results)):
			outFile.write(sortRes[x]+","+str(counts[results.index(sortRes[x])])+u"\n")
		#print results

	if inCommand == u"span":
		inFileName=inArgument.split(" ")[0]
		outFileName=inArgument.split(" ")[1]
		booln=span_DB(inFileName,outFileName)
		if booln:
			print "success"
		else:
			print "failure"

	if inCommand == u"matchaddress":
		inFileName=inArgument.split(" ")[0]
		listFileName=inArgument.split(" ")[1]
		outFileName=inArgument.split(" ")[2]
		log = 1
		if inArgument.split(" ")[3]=="writelog":
			log=0
		if len(inArgument.split(" "))>4:
			autoP=int(inArgument.split(" ")[4])
			booln=match_with_address_list(inFileName, listFileName, outFileName, log, autoPilotStartsAt=autoP)
		else:
			booln=match_with_address_list(inFileName, listFileName, outFileName, log)

		if booln:
			print "success"
		else:
			print "failure"

	if inCommand == u"savenames":
		inFileName=inArgument.split(" ")[0]
		colNo=int(inArgument.split(" ")[1])
		booln = save_names(inFileName,colNo,"this","that")

	if inCommand== u"matchfnames":
		inFileName=inArgument.split(" ")[0]
		clean_firstnames(inFileName)