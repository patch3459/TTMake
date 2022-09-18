from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.support import expected_conditions as ec
#from selenium.webdriver.support.ui import WebDriverWait
import time
import os 

class ImageRenderer:

	'''
	ImageRenderer Class

	uses selenium/webdrver to obtain screenshots of particular reddit threads
	'''

	options = Options()
	#options.add_argument("--headless")
	options.add_argument("--window-size=100,1920") #for some reason 1080 didn't work on my pc, ymmv
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-popup-blocking")
	options.add_argument("--incognito")
	#options.add_argument("--load-extension=\'adblock.crx\'")

	def __init__(self):

		'''
		__init__
		initializes the webdriver, in this case I use chrome, but you can change it manaully but ymmv
		'''
		self.driver = webdriver.Chrome(options=self.options) #install webdriver too

	def getTitleTextImage(self,url, folder, name):
		self.driver.get(url)

		time.sleep(2)
		if len(self.driver.find_elements(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']" )) != 0:
			btn1 = self.driver.find_element(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']//button[@Class=\'i2sTp1duDdXdwoKi1l8ED _2iuoyPiKHN3kfOoeIQalDT _2tU8R9NTqhvBrhoNAXWWcP HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0\']")
			btn1.click()

			time.sleep(2)

			btn2 = self.driver.find_element(By.XPATH, "//button[@Class=\'gCpM4Pkvf_Xth42z4uIrQ\']")
			btn2.click()


		time.sleep(2)
		element = self.driver.find_element(By.XPATH, '//h1[@Class=\'_eYtD2XCVieq6emjKBH3m\']') # the title class
		with open(os.path.join(folder,name), "wb+") as f:
			f.write(element.screenshot_as_png)
			time.sleep(.1)

		self.driver.close()

	def getTitleImage(self,url, folder, name):
		self.driver.get(url)

		time.sleep(2)
		if len(self.driver.find_elements(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']" )) != 0:
			btn1 = self.driver.find_element(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']//button[@Class=\'i2sTp1duDdXdwoKi1l8ED _2iuoyPiKHN3kfOoeIQalDT _2tU8R9NTqhvBrhoNAXWWcP HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0\']")
			btn1.click()

			time.sleep(2)

			btn2 = self.driver.find_element(By.XPATH, "//button[@Class=\'gCpM4Pkvf_Xth42z4uIrQ\']")
			btn2.click()


		time.sleep(2)
		element = self.driver.find_element(By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),\'_1oQyIsiPHYt6nx7VOmd1sz _2rszc84L136gWQrkwH6IaM\')]") # the title class
		with open(os.path.join(folder,name), "wb+") as f:
			f.write(element.screenshot_as_png)
			time.sleep(.1)

		self.driver.close()

	def getParagraphs(self,url, folder):
		self.driver.get(url)

		time.sleep(2)
		if len(self.driver.find_elements(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']" )) != 0:
			btn1 = self.driver.find_element(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']//button[@Class=\'i2sTp1duDdXdwoKi1l8ED _2iuoyPiKHN3kfOoeIQalDT _2tU8R9NTqhvBrhoNAXWWcP HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0\']")
			btn1.click()

			time.sleep(2)

			btn2 = self.driver.find_element(By.XPATH, "//button[@Class=\'gCpM4Pkvf_Xth42z4uIrQ\']")
			btn2.click()


		paragraphs = self.driver.find_elements(By.XPATH, "//div[@data-test-id=\'post-content\']//p[@class=\'_1qeIAgB0cPwnLhDF9XSiJM\']")

		for index, p in enumerate(paragraphs):
			with open(os.path.join(folder, f"img{index + 1}.png"), "wb+") as f:
				f.write(p.screenshot_as_png)

		self.driver.close()


	def getTitleAndParagraphs(self,url, folder):
		'''
		primarily for storytime style subreddits.

		Will use chromedriver to get the title screen shots and paragraphs

		implementation atm is wonky because of some weird bugs on my end. 
		'''


		self.driver.get(url)


		# if it's nsfw
		time.sleep(2)
		if len(self.driver.find_elements(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']" )) != 0:
			btn1 = self.driver.find_element(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']//button[@Class=\'i2sTp1duDdXdwoKi1l8ED _2iuoyPiKHN3kfOoeIQalDT _2tU8R9NTqhvBrhoNAXWWcP HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0\']")
			btn1.click()

			time.sleep(2)

			btn2 = self.driver.find_element(By.XPATH, "//button[@Class=\'gCpM4Pkvf_Xth42z4uIrQ\']")
			btn2.click()



		# WORKAROUND FOR THE REDDIT POSTS

		self.driver.execute_script('''
			let val = document.getElementsByClassName(\'_292iotee39Lmt0MkQZ2hPV RichTextJSON-root\')[0].lastChild.innerHTML;
			 n = document.createElement(\'p\');
			 n.className = \'_1qeIAgB0cPwnLhDF9XSiJM\'; 
			 n.innerHTML = val;   
			document.getElementsByClassName(\'_292iotee39Lmt0MkQZ2hPV RichTextJSON-root\')[0].appendChild(n);
			''')
		'''
		What's going on ^^^ and in the os.remove and os.rename?

		Well in a reddit text, the website's lastChild will have zero bottom padding. Ostensibly the chromedriver is using the top and
		bottom padding to make a screenshot and locate the element. I'm not entirely sure why that element is broken so I just duplicate
		the element and replace the screenshot :/ in the future though it might be fixed. Might have to do with this version of chromedriver
		'''
		time.sleep(0.1)

		#title
		time.sleep(2)
		element = self.driver.find_element(By.XPATH, '//h1[@Class=\'_eYtD2XCVieq6emjKBH3m\']') # the title class

		#screenshotting every element
		with open(os.path.join(folder,"img0.png"), "wb+") as f:
			f.write(element.screenshot_as_png)

		paragraphs = self.driver.find_elements(By.XPATH, "//div[@data-test-id=\'post-content\']//p[@class=\'_1qeIAgB0cPwnLhDF9XSiJM\']")

		#paragraphs
		length = len(paragraphs) + 1
		for index, p in enumerate(paragraphs):

			with open(os.path.join(folder, f"img{index + 1}.png"), "wb+") as f:
				f.write(p.screenshot_as_png)
				time.sleep(.01)


		'''
		Bug fix pt. 2. The bottom item has zero bottom padding and the item doesn't seem to be ss right
		so we replace this new item in....
		'''
		os.remove(os.path.join(folder, f"img{length - 2}.png"))
		os.rename(os.path.join(folder, f"img{length-1}.png") , os.path.join(folder, f"img{length-2}.png"))

		self.driver.close()

	def getTopComments(self,url, folder, limit, isSerious=False):

		'''
		Gets the parent comment of a particular num of threads in reddit
		'''

		self.driver.get(url)


		# if it's nsfw
		time.sleep(2)
		if len(self.driver.find_elements(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']" )) != 0:
			btn1 = self.driver.find_element(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']//button[@Class=\'i2sTp1duDdXdwoKi1l8ED _2iuoyPiKHN3kfOoeIQalDT _2tU8R9NTqhvBrhoNAXWWcP HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0\']")
			btn1.click()

			time.sleep(2)

			btn2 = self.driver.find_element(By.XPATH, "//button[@Class=\'gCpM4Pkvf_Xth42z4uIrQ\']")
			btn2.click()

		'''WebDriverWait(self.driver, 5).until(
			ec.presence_of_element((By.ID, "ScrrUjzznpAqm92uwgnvO"))
			)'''

		topComments = self.driver.find_elements(By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),\'P8SGAKMtRxNwlmLz1zdJu HZ-cv9q391bm8s7qT54B3 _1z5rdmX8TDr6mqwNv7A70U\')]")
		

		#another work around b/c i cant get the ad block to work :( 

		time.sleep(1)
		#paragraphs

		count = 0
		for index, p in enumerate(topComments):

			if count == limit:
				break

			p.location_once_scrolled_into_view

			self.driver.execute_script("window.scrollBy(0,-100);")

			time.sleep(2)



			if index == 0 and isSerious:
				assert 1 == 2 # sometimes there's a bot comment or a "serious comment"


			with open(os.path.join(folder, f"img{count + 1}.png"), "wb+") as f:
				f.write(p.screenshot_as_png)
				count += 1
				time.sleep(.01)


	def getCommentParagraphs(self,url, folder):

		'''
		Gets the parent comment of a particular num of threads in reddit
		'''

		self.driver.get(url)


		# if it's nsfw
		time.sleep(2)
		if len(self.driver.find_elements(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']" )) != 0:
			btn1 = self.driver.find_element(By.XPATH, "//div[@Class=\'bDDEX4BSkswHAG_45VkFB\']//button[@Class=\'i2sTp1duDdXdwoKi1l8ED _2iuoyPiKHN3kfOoeIQalDT _2tU8R9NTqhvBrhoNAXWWcP HNozj_dKjQZ59ZsfEegz8 _2nelDm85zKKmuD94NequP0\']")
			btn1.click()

			time.sleep(2)

			btn2 = self.driver.find_element(By.XPATH, "//button[@Class=\'gCpM4Pkvf_Xth42z4uIrQ\']")
			btn2.click()

		topComment = self.driver.find_elements(By.XPATH, "//div[contains(concat(' ',normalize-space(@class),' '),\'P8SGAKMtRxNwlmLz1zdJu HZ-cv9q391bm8s7qT54B3 _1z5rdmX8TDr6mqwNv7A70U\')]")[0]
		

		#another work around b/c i cant get the ad block to work :( 

		time.sleep(1)
		#paragraphs

		count = 0
		for index, p in enumerate( self.driver.find_elements(By.XPATH, "//p[@Class=\'_1qeIAgB0cPwnLhDF9XSiJM\']" )):
			p.location_once_scrolled_into_view

			self.driver.execute_script("window.scrollBy(0,-100);")

			time.sleep(1)

			with open(os.path.join(folder, f"img{count + 1}.png"), "wb+") as f:
				f.write(p.screenshot_as_png)
				count += 1
				time.sleep(.01)