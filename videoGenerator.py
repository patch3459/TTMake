#from email.mime import base
from speechToText import makeAudio
from redditParser import Scraper
from imageGenerator import createAssets
from util import listAll

from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip, CompositeAudioClip
from moviepy.video.fx.resize import resize

import librosa
import os


def generateVideo(audioFolder,imageFolder,baseVideo, targetFolder, targetName, baseAudio=None):
	'''
	Tries to generate a video using the audio assets, base assets, image assets.

	DOES NOT CREATE THE AUDIO AND IMAGE ASSETS. For that, you'll need to look at
	imageGenerator.py and speechToText.py
	'''
	os.mkdir(targetFolder)
	
	baseClip = VideoFileClip(baseVideo).without_audio() # removing the game audio

	baseClipWidth, baseClipHeight = baseClip.size

	compositeAudioList = [AudioFileClip] if not baseAudio is None else []
	compositeImageClipList = []
	currentTime = 0

	for index, file in enumerate(listAll(audioFolder, ".mp3")):
		# because util.listAll() returns a sorted list by modification time should align with file

		#seconds
		audioClipLength = librosa.get_duration(filename=file)

		audioClip = AudioFileClip(file).set_start(currentTime).set_duration(audioClipLength)
		imageClip = ImageClip(
			os.path.join(imageFolder,f"img{index}.png")
			).set_start(currentTime).set_duration(audioClipLength).set_position(("center","center")).resize(1.0)

		currentTime += 0.1 
		currentTime += audioClipLength

		compositeImageClipList.append(imageClip)
		compositeAudioList.append(audioClip)

	baseClip = baseClip.loop(duration=currentTime)

	final = CompositeVideoClip([baseClip.set_duration(currentTime + 0.1)] + compositeImageClipList)
	final.audio = CompositeAudioClip(compositeAudioList)
	final.write_videofile(os.path.join(targetFolder, targetName))




