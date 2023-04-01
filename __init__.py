# -*- coding: utf-8 -*-
# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo
from aqt.utils import showText
# import all of the Qt GUI library
from aqt.qt import *
# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

import mylogging

#The Deck ih whch are all cards will instered
deckName = "English"

# returns array of ("dupestr", [nids])
#def findDupes(col, fieldName, search=""):

#Suche Karten ohne Suund auf der vorderseite
#deck:English  card:1 -front:*[sound:*


#Kopiere auf Smartphone
#adb push collection.apkg /sdcard/AnkiDroid/collection.apkg


def isAlreadyInCollection(front):
	ids = mw.col.findCards("deck:" + deckName +" card:1 front:" + front + "*")
	return len(ids) > 0

def addCard(front,back):
	#Replace new lines
	#We Don't want a line break at the fist charter
	if back and back[0] == '\n':
		back = back[1:]
	if front and front[0] == '\n':
		front = front[1:]
	front = front.replace("\n", "<br />")
	back = back.replace("\n", "<br />")
	#Set Style
	back = "<div style='margin:auto;display: inline-block;align: center;text-align: left;'>" + back + "</div>" 	
	
	#Add Card
	mylogging.info(u"Add Card: " + unicode(front) + u" Back: " + unicode(back))
	deckId = mw.col.decks.byName(deckName)["id"]
	assert deckId != None
	cardCount = mw.col.cardCount()
	#showInfo("Card count: %d" % cardCount)
	m = mw.col.models.current()
	m['did'] = deckId
	mw.col.models.save(m)
	n = mw.col.newNote()
	n['Front'] = front
	n['Back'] = back
	if not n.dupeOrEmpty():
		mw.col.addNote(n)
	

def printInsertResults(cardsToInsert,cardsNotToInsert):
	import functools
	def compare(item1, item2):
		return item1["front"] < item2["front"]
	sorted(cardsToInsert, key=functools.cmp_to_key(compare))
	sorted(cardsNotToInsert, key=functools.cmp_to_key(compare))
	a = len(cardsToInsert)
	b = len(cardsNotToInsert)
	if a + b == 0:
		mylogging.info("Nothing Changed")
		return
	mylogging.info("Cards inserted: " + str(a) + " Not inserted: " + str(b) + "(" + str(float(b) / float(a + b))  + "%)")
	mylogging.info("Following cards are inserted...")
	for card in cardsToInsert:
		mylogging.info("Card: " + card["front"])
	mylogging.info("===============================")
	mylogging.info("Following cards arn't inserted...")
	for card in cardsNotToInsert:
		mylogging.info("Card: " + card["front"] + " Reason: " + card["error-text"])

def testFunction():
	#Load all data
	import database
	import flashcardmaker
	dataSet = database.loadDatabase()
	#dataSet = [["hapless"]] NOTE Testdataset
	mylogging.info("Load entries from db:" + str(len(dataSet)))
	#Try to create cards
	#import en
	cardsToInsert = []
	cardsNotToInsert = []
	for e in dataSet:
		card = flashcardmaker.createCard(e[0])
		altSearch=card["alt-search"]
		if card["error"]:
			cardsNotToInsert.append(card)
		elif (isAlreadyInCollection(card["front"]) or (len(altSearch) and isAlreadyInCollection(altSearch))):
			card["error-text"] = " already in collection"
			cardsNotToInsert.append(card)
		else:
			cardsToInsert.append(card)
			addCard(card["front"],card["back"])
	#for x in cardsToInsert:
	#	mylogging.info("Add Card: " + str(card["front"]) + " Back: " + str(card["back"]))
		#addCard(card["front"],card["back"])
			
	printInsertResults(cardsToInsert,cardsNotToInsert)
	#Check Anki for duplicates
	mylogging.info("finish")
    

		
    
# create a new menu item, "test"
action = QAction("yggdrasil", mw)
# set it to call testFunction when it's clicked
action.triggered.connect(testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
