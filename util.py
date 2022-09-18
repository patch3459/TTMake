'''
misc utils used throughout the project.
'''
import os
from pathlib import Path
from markdown import markdown
from bs4 import BeautifulSoup
import re

def listAll(folder, extension):
	fileList = []

	for file in sorted(Path(folder).iterdir(), key=os.path.getmtime):
		if file.__str__().endswith(extension):
			fileList.append(file.__str__())

	return fileList

def createFolders(name):
	name = f"{name}"
	os.mkdir(f"{name}")
	os.mkdir(f"{name}/audio")
	os.mkdir(f"{name}/img")

	return {
		"root":name,
		"audio":f"{name}/audio",
		"img":f"{name}/img"
		}

def isAlphabetic(string):
	for char in string:
		if not char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz":
			return False
	return True


def markdownToPlaintext(md):
	'''
	Returns the plaintext of md
	'''

	html = markdown(md)
	html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
	html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
	soup = BeautifulSoup(html, "html.parser")
	text = ''.join(soup.findAll(text=True))
	
	return text	


#print(os.listdir("./tmp/video0/img"))