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

# this code fixes the problem that in the address_whitelist.txt streets labeled "-utcza" instead of " utcza" are coded as roads, not streets

inFileName="address_whitelist.txt"
outFileName="address_whitelist_fixed.txt"

inFile = codecs.open(inFileName,'r', encoding='utf-8', errors='replace')

outFile = codecs.open(outFileName,'w', encoding='utf-8', errors='replace')

for lines in inFile:
	listitem = lines.split(',')
	if u"-utcza" in listitem[3] and int(listitem[2])==2:
		listitem[2]="1"
	newline=",".join(listitem)
	outFile.write(newline)
