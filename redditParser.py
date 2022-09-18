import praw
from psaw import PushshiftAPI
from util import isAlphabetic, markdownToPlaintext

class Scraper:
	'''
	Scraper Class

	Probes the psaw API to return submissions, content, etc
	
	'''
	def __init__(self,username, pwd, c_id, c_secret, useragent):
		self.client = praw.Reddit(
			client_id=c_id,
			client_secret=c_secret,
			password=pwd,
			username=username,
			user_agent=useragent,
			)
		self.api = PushshiftAPI(self.client)

	def getHotPosts(self, subreddit, limit):
		return self.client.subreddit(subreddit).hot(limit=limit)

	def scrapeTexts(self, subreddit, query, limit):
		'''
		Queries a subreddit for submissions.

		Returns a list of praw.submissions
		'''
		results = self.api.search_submissions(
			q = query,
			subreddit = subreddit,
			sort_type='score',
			#filter=['score'],
			limit = limit)

		return list(results)

	def parseSubmission(self, submission):
		return {
			"title" :submission.title,
			"text" : self.listParagraphs(submission), # paragraphing the 
			"url" : submission.url,
		}

	def listParagraphs(self, submission):
		return [p for p in submission.selftext.split("\n") if p != "" and isAlphabetic(p)]

	def getSubmissionByUrl(self, url):
		'''
		gets a praw Submission Object via it's constructor with the url

		the link does need to be comparible with a particular method, but I haven't the
		chance to fix it. See below

		https://praw.readthedocs.io/en/stable/code_overview/models/submission.html#praw.models.Submission.id_from_url
		'''
		try:
			return praw.models.Submission(self.client, url=url)
		except Exception as e:
			return f"Error: {e}"


	def getCommentByUrl(self, url):
		return self.client.comment(url)

	def getCommentParagraphs(self, comment):
		return [ markdownToPlaintext(p) for p in comment.body.split("\n")]


	def getParentSubmission(self, comment):
		return self.client.submission(
			comment.link_id
		)

	def listParagraphsByUrl(self, url):
		'''
		Uses getSubmissionByUrl() to print paragraphs similar to listParagraphs()
		'''
		return self.listParagraphs(
			self.getSubmissionByUrl(url)
		)
	
	def parseSubmissionByUrl(self, url):
		'''
		Same behaviour as parseSubmission() using getSubmmissionByUrl()
		'''
		return self.parseSubmission(
			self.getSubmissionByUrl(url)
		)

	def isSubmissionSerious(self, submission):

		return submission.title.find("[Serious]") != -1

	def scrapeTopComments(self, submission, limit):
		'''
		takes a praw submission and returns a list of 
		reddit comments of size limit

		these comments are all top level comments

		for more on the sorting see below
		https://praw.readthedocs.io/en/stable/getting_started/quick_start.html?highlight=comment_sort#obtain-comment-instances
		'''

		submission.comment_sort = "best"

		comments = []


		count = 0
		for item in submission.comments:
			if count == limit:
				break

			try:
				if item.author.name == "AutoModerator" or markdownToPlaintext(item.body) == "[deleted]" or markdownToPlaintext(item.body) == "[removed]":
					continue

			except AttributeError as e:
				print(f'Possible error? ')
				continue

			comments.append(markdownToPlaintext(item.body))
			count += 1
		
		return comments