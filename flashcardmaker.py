#!/usr/bin/python
# -*- coding: utf-8 -*-
#https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation
#The lib must be on the same level like the root script
import sys
sys.path.append('../')
import en
import MerriamWebster


def normalizeWord(word):
	"""Remove some annoying chars at the of the string"""
	forbiddenChars = {'.',',','?','!',":",";"}
	for x in forbiddenChars:
		word = word.replace(x,"")
	return word.lower()



#	"""Try to create a flash card from a String
#    Return a Map:
#    error -- True in case of an error
#    error-text -- the error text
#    front	-- the front site of the card
#    back -- the backsite of the card"""
#    alt-search - ein Alternativer Suchbegriff
def createCard(word):
	word = normalizeWord(word)
	if not word:
		return {"error" : True,"error-text" : "empty string"}
	else:
		return lookUpWord(word)

def lookUpWord(word):
	back = MerriamWebster.lookUpWord(word)
	if  back != None:
		return {"error" : False,"front" : word,"back" : back,"error-text" : "","alt-search" : ""}
	return lookUpWordEn(word)

	
def lookUpWordEn(word):
	"""
	Lookup a String in a dict and return a flash card suggestion
	"""
	copyOfWord = word
	#word = normalizeWord(word)
	front = word
	back = ""
	errorText = ""
	found = True
	altSearch=""
	#We don't want the plural here
	if en.is_noun(word):
		word = en.noun.singular(word)
		front = word
		back = en.noun.gloss(word)
	elif en.is_verb(word):
		word = en.verb.infinitive(word)
		back = en.verb.gloss(word)
		altSearch = word
		front = "to " + word
	elif en.is_adjective(word):
		#TODO Steigerung auf grundfrom
		back = en.adjective.gloss(word)
		front = word
	elif en.is_adverb(word):
		back = en.adverb.gloss(word)
		front = word
	else:
		found = False
		errorText = word + " not found in a dict"
	if found and not back:
		found = False
		errorText = " back is empty"
	return {'error': not found,"front" : front,"back" : back,"error-text": errorText,"alt-search" : altSearch}
