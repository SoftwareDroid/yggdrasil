#!/usr/bin/python
# -*- coding: utf-8 -*-

#TODO Rausfiltern 


#Global contants
WORKING_INDEX = 0
ALL_TEXT_INDEX = 1
ALL_TEXT2_INDEX = 2
NEED_WORD_TYPE_INDEX = 3

#Gebe None zurück wenn kein Eintrag gefunden wurde

import urllib2
from BeautifulSoup import BeautifulSoup
import re
#Entfernt Zahlen direkt am Wort Ende
filter1 = re.compile(r"([a-zA-Z])(\d\D?)([\,\s$])")
#Zahl Space colon -> Zahl colon
filter2 = re.compile(r"(\d)(\s)(:)")

def lookUpWord(word):
	try:
		soup = BeautifulSoup(urllib2.urlopen('http://www.wordcentral.com/cgi-bin/student?book=Student&va=' + word).read())
	except urllib2.HTTPError as err:
		return None
	#Get body
	body = soup.body
	#Get <div id="leftCol">
	body = body('div', {'id': 'body'})[0]
	#Get <div id="leftCol">
	#Verwandle in String und Suche Anfang
	test = body('div',{'id': 'leftCol'})[0]
	return tryExtractFormat1(test)

def normalizeWord(word):
	#Reduce space
	word = limitSpace(word)
	#Entfernt Zahlen direkt am Wort Ende
	word = filter1.sub(r"\1\3",word)
	#Zahl Space colon -> Zahl colon
	word = filter2.sub(r"\1\3",word)
	#Insert < and >
	word = word.replace("&lt;","<")
	word = word.replace("&gt;",">")
	return word

	
#Begrenzt die Anzahl der Definition die zurückkommen können	
def limitSpace(word):	
	def isInt(value):
	  try:
		int(value)
		return True
	  except:
		return False
	counter = 0
	maxCounter = 4
	parts = word.split("\n")
	text = ""
	for x in parts:
		if len(x) >= 1 and isInt(x[0]):
			counter = counter + 1
		if counter <= maxCounter:
			text += "\n" + x
		else:
			break
	return text

#Verarbeitet einen Link und gibt an ob dieser relevant ist, für die defintion eines Wortes
def isLinkRelevant(tag):
	assert (tag.name == "a"),"Only 'a' tags are valid!"
	if bool(tag.get("href")):
		#print "Print Link Text: " + str(tag.get("href")) + " OK:" + str(tag.get("href").startswith(u"student?book"))
		if tag.get("href").startswith(u"student?book=Student&va"):
			return True
	return False

#Return Tupel [working,allText,allText2,needWordType]
def parseTag(atts,currentTag):
	#Start Algo
	allElements = currentTag.contents
	for val in allElements:
		if atts[WORKING_INDEX]:
			if str(type(val)) == "<class 'BeautifulSoup.Tag'>":
				#Der erste Tag der kommen sollte ist wordType
				if atts[NEED_WORD_TYPE_INDEX] and val.name == 'i':
					atts[ALL_TEXT_INDEX] += "Function: " + val.string
					atts[NEED_WORD_TYPE_INDEX] = False
				#Verarbeite alle Zeilenumbrücke 1 zu 1	
				elif val.name == "br":
					#Komplette leere Zeilen werden später rausgefiltert
					atts[ALL_TEXT_INDEX] += "\n"
				#Italic text ist Ok	
				elif val.name == "i":
					if 	val.string != None:
						atts[ALL_TEXT_INDEX] += val.string
					else:
						 atts = parseTag(atts,val)
				elif val.name == 'b':
					if val.string != None:
						atts[ALL_TEXT_INDEX] += val.string
					else:
						atts = parseTag(atts,val)
				elif val.name == 'a' and isLinkRelevant(val):
					atts[ALL_TEXT_INDEX] += val.text
			elif str(type(val)) == "<class 'BeautifulSoup.NavigableString'>":
				#Ignore simple spaces
				atts[ALL_TEXT_INDEX] += str(val)
		else:
			#Finde den Anfang ab wann geparst werden soll
			if "Function:" in val:
				atts[WORKING_INDEX] = True
		#Update all Text2
		atts[ALL_TEXT2_INDEX] = atts[ALL_TEXT_INDEX]
	return atts


	
def tryExtractFormat1(tag):
	#print tag.prettify()
	#We want a unicode strings
	allText2 = u""
	allText = u""
	needWordType = True
	working = False
	#Retrieve result
	atts = parseTag([working,allText,allText2,needWordType],tag)
	working = atts[WORKING_INDEX]  
	allText = atts[ALL_TEXT_INDEX]
	#Strip at beign and end	
	allText = allText.strip()
	#Remove multible newlies
	while allText.find("\n\n") != -1:
		allText = allText.replace('\n\n','\n')
	#if we havn't found a start return none
	if not working:	
		return None
	return normalizeWord(allText) 
