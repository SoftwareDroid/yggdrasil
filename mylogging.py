# -*- coding: utf-8 -*-

import logging
import os

#Clear the file before writing
logFile = os.path.expanduser("~/Desktop/plugin-log.txt")
with open(logFile, "w") as file:
	file.truncate()

logging.basicConfig(filename=logFile,level=logging.DEBUG)


def debug(text):
	logging.debug(text)

def info(text):
	logging.info(text)
	
def warning(text):
	logging.warning(text)
