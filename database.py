# -*- coding: utf-8 -*-

# import the "show info" tool from utils.py
from aqt.utils import showInfo

def loadDatabase():
	import os
	filename = os.path.expanduser("~/Desktop/KoboReader.sqlite")
	if checkFile(filename):
		import sqlite3
		conn = sqlite3.connect(filename)
		c = conn.cursor()
		#fetch all data
		c.execute("SELECT Text FROM Bookmark WHERE Text is not NULL")
		#Remove Duplicates
		from collections import OrderedDict
		return list(OrderedDict.fromkeys(c.fetchall()))
	return list()
	
def checkFile(filename):
	import os.path
	if not os.path.isfile(filename):
		showInfo("The file " + filename + " does't exist!")
		return False
	return True
