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

from process_geo import *
from process_basics import *
from process_commands import *







########################################################################################################################################
#### PROGRAM'S MAIN PART: EXECUTES USER COMMANDS
########################################################################################################################################

defaultInputFileName="data.txt"
defaultCommandFileName="processcommands.txt"
inputFile=defaultInputFileName
outputFile=defaultCommandFileName

readCommand = 0

if len(sys.argv)==1:
	print "no command read as argument - proceeding with manual read"
	command=u""
	argument=u""
	while command!="q":
		[command,argument]=read_command_from_KB()
		if command == u"f":
			where = -1
			if contains_digits(argument.split(" ")[0]):				
				where=int(argument.split(" ")[0])
			print type(argument)
			#argument.decode('utf-8')
			if argument=='á'.encode('ascii'):
				print argument
			unicode(argument)
			results=find_in_database(inputFile,argument,where)
			for elements in results:
				if len(elements)==1:
					print elements.encode('utf-8')
				if len(elements)>1:
					print elements[0].encode('utf-8')+" times: "+str(elements[1])


if len(sys.argv)>1:
	if sys.argv[1]=="r":
		print "reading commands from file\n"
		cmdList=read_process_commands(outputFile)
		print cmdList
		for elements in cmdList:
			command=elements[0]
			argument=elements[1]
			#print command.encode('utf-8')
			#print argument.encode('utf-8')
			do_command(inputFile,command,argument)



