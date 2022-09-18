'''
	A module filled with render functions for all sorts of tiktok / shorts needs!

'''
from json import load
from speechToText import makeAudio
from redditParser import Scraper
from videoGenerator import generateVideo
from renderImages import ImageRenderer
from util import createFolders

from datetime import datetime
from dotenv import dotenv_values
import os
import shutil
import traceback

# single use 



def storytimeByQuery(subreddit, query, limit, baseVideo, baseAudio=None):


	time = datetime.now().strftime("%Y%m%d-%H%M%S")

	os.mkdir(f"./tmp/{time}")


	config = dotenv_values(".env")
	s = Scraper(
		config["USERNAME"],
		config["PWD"],
		config["CLIENT_ID"],
		config["CLIENT_SECRET"],
		config["USER_AGENT"])

	submissions = s.scrapeTexts(subreddit, query, limit)
	videosMade = 0

	for index, submission in enumerate(submissions):
		try: 
			if videosMade == limit:
				print(f"{limit} videos successfully made!")
				break

			folders = createFolders(f"./tmp/{time}/video{index}")

			submission_data = s.parseSubmission(submission)

			if submission_data["text"] == [] or str(submission_data['text']).find("[deleted]") != -1 or str(submission_data['text']).find("[removed]") != -1:
				continue

			makeAudio( 
				[s.lower() for s in [submission_data['title']] + submission_data["text"]], 
				folders["audio"] )

			ImageRenderer().getTitleAndParagraphs(submission_data["url"], folders["img"])

			now = datetime.now().strftime("%Y%m%d-%H%M%S")


			generateVideo(
				folders["audio"],
				folders["img"],
				baseVideo,
				f"./videos/{now}",
				f"video{index}.mp4"
				)
			print(f"Created video{index}.mp4")
			videosMade += 1

		except Exception as e:
				print(f"Error at video{index} : {traceback.format_exc()}")
				continue

	#shutil.rmtree(f"./tmp")

def storytime(url, limit, baseVideo, videoName, baseAudio=None):
	time = datetime.now().strftime("%Y%m%d-%H%M%S")

	os.mkdir(f"./tmp/{time}")

	# VVV change the Scraper for your own client
	config = dotenv_values(".env")
	s = Scraper(
		config["USERNAME"],
		config["PWD"],
		config["CLIENT_ID"],
		config["CLIENT_SECRET"],
		config["USER_AGENT"])



	try: 
			submission = s.getSubmissionByUrl(url)
			top_comments = s.scrapeTopComments(submission, limit)

			submission_url = submission.url
			title = submission.title

			folders = createFolders(f"./tmp/{time}/video")

			submission_data = s.parseSubmission(submission)

			if submission_data["text"] == [] or str(submission_data['text']).find("[deleted]") != -1 or str(submission_data['text']).find("[removed]") != -1:
				shutil.rmtree(f"./tmp/{time}")
				return

			makeAudio( 
				[s.lower() for s in [submission_data['title']] + submission_data["text"]], 
				folders["audio"] )

			ImageRenderer().getTitleAndParagraphs(submission_data["url"], folders["img"])

			now = datetime.now().strftime("%Y%m%d-%H%M%S")


			generateVideo(
				folders["audio"],
				folders["img"],
				baseVideo,
				f"./videos/{now}",
				f"storytime{index}.mp4"
				)
			print(f"Created {videoName}.mp4")
			videosMade += 1

	except Exception as e:
				print(f"Error at {videoName} : {traceback.format_exc()}")
				shutil.rmtree(f"./tmp")
				return
				

	#shutil.rmtree(f"./tmp")

def askReddit(url,limit, baseVideo, destinationFolder,videoName,audio_code):
	time = datetime.now().strftime("%Y%m%d-%H%M%S")

	os.mkdir(f"./tmp/{time}")
	# VVV change the Scraper for your own client
	config = dotenv_values(".env")
	s = Scraper(
		config["USERNAME"],
		config["PWD"],
		config["CLIENT_ID"],
		config["CLIENT_SECRET"],
		config["USER_AGENT"])



	try: 
			submission = s.getSubmissionByUrl(url)



			top_comments = s.scrapeTopComments(submission, limit)

			submission_url = submission.url
			title = submission.title

			folders = createFolders(f"./tmp/{time}/video")

			makeAudio([title] + top_comments, folders["audio"], audio_code )
			ImageRenderer().getTitleImage(submission_url, folders["img"], "img0.png")

			isSerious = s.isSubmissionSerious(submission)
			ImageRenderer().getTopComments(submission_url, folders["img"], limit, isSerious=isSerious)

			now = datetime.now().strftime("%Y%m%d-%H%M%S")
			generateVideo(
				folders["audio"],
				folders["img"],
				baseVideo,
				f"./videos/{now}",
				f"{videoName}.mp4",
				)

			print(f"Created {videoName}.mp4")

	except Exception as e:
				print(f"Error at {videoName} : {traceback.format_exc()}")

	#shutil.rmtree(f"./tmp")



#make multiple 


def multipleAskReddit( query, limit, baseVideo, baseAudio=None):

	'''

	Still in development
	'''
	config = dotenv_values(".env")
	s = Scraper(
		config["USERNAME"],
		config["PWD"],
		config["CLIENT_ID"],
		config["CLIENT_SECRET"],
		config["USER_AGENT"])


	submissions = s.scrapeTexts("askreddit", query, limit)
	videosMade = 0


	for index, submission in enumerate(submissions):
		if videosMade == limit:
			break
		
		
		askReddit(submission.url, 5, baseVideo, f"ask_reddit_video{index}", baseAudio,)
		videosMade += 1
	print(f"Successfully made {limit} videos!")


def askRedditComment(url, baseVideo, videoName, baseAudio=None):
	time = datetime.now().strftime("%Y%m%d-%H%M%S")

	os.mkdir(f"./tmp/{time}")
	# VVV change the Scraper for your own client
	config = dotenv_values(".env")
	s = Scraper(
		config["USERNAME"],
		config["PWD"],
		config["CLIENT_ID"],
		config["CLIENT_SECRET"],
		config["USER_AGENT"])



	try: 
			comment = s.getCommentByUrl(url)

			comment_paragraphs = s.getCommentParagraphs(comment)

			parent_submission = s.getParentSubmission(comment)

			title = parent_submission.title
			
			folders = createFolders(f"./tmp/{time}/video")


			makeAudio([title] + comment_paragraphs, folders["audio"] )
			ImageRenderer().getTitleImage(url, folders["img"], "img0.png")

			ImageRenderer().getCommentParagraphs(url, folders["img"])

			now = datetime.now().strftime("%Y%m%d-%H%M%S")
			generateVideo(
				folders["audio"],
				folders["img"],
				baseVideo,
				f"./videos/{now}",
				f"{videoName}.mp4",
				baseAudio=baseAudio
				)

			print(f"Created {videoName}.mp4")

	except Exception as e:
				print(f"Error at {videoName} : {traceback.format_exc()}")
