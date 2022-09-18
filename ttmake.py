import argparse
import os 
from dotenv import dotenv_values
from datetime import datetime

from renderReddit import askReddit 
'''

ttmake : a utility for generating AskReddit Style TikTok videos using
Selenium, MoviePy, and PRAW/PSAW. By default, ttmake will use a config file
stored inside of the utilities folder, use the argument --find_config_file to
find the directory it's in. For the config file, you do need to fill in your
reddit information. Go to https://github.com/patch3459/TT_Autom8 for the
source code or if you have any questions.

At the moment there is only the askReddit() functionality, but I hope in the future to
be able to support more subreddits and whatnot.

I probably won't be maintaining this project, so feel free to fork it so long as you use proper credit.

There are a lot of functions within renderReddit.py that work, but they aren't currently supported via CLI.
You can of course plug it into this TTMAKE file, but it might be a pain because of the changes being made elsewhere

Best regards and god bless!

Patch


'''

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description = "ttmake : a utility for generating AskReddit Style TikTok videos using Selenium, MoviePy, and PRAW/PSAW. By default, ttmake will use a config file stored inside of the utilities folder, use the argument --find_config_file to find the directory it's in. For the config file, you do need to fill in your reddit information. Go to https://github.com/patch3459/TT_Autom8 for the source code or if you have any questions.")

	parser.add_argument("link", type=str,nargs="?", default="" ,help="A reddit link to generate the video from, if you use --use_text_file or -u it will read in the list of reddit links seprated by a newline")

	parser.add_argument("-a", type=int, default=0, help="Which text-to-speech service to use. By default it will use Amazon Polly, but use the following system to determine which one you would like to use. 0 : Amazon Polly, 1: Microsoft Azure TTS (requires key in .env file), 2: Google Trasnslate TTS, 3: Balbonka CLI (requires local CLI installation)")

	parser.add_argument("-p", type=str, default=".", help="Where to save the videos to. ttmake will create a folder in that directory with those videos inside")

	parser.add_argument("-l", type=int, default=5, help="Max amount of comments to parse. By default it's 5")

	#optional args/flags

	parser.add_argument("-v", default="",type=str,help="Path to the video file to use for the background of the video. This will overwrite the .env file's video")

	parser.add_argument("-u", "--use_text_file",action="store_true", help="Will tell ttmake to read link argument as a text file")

	parser.add_argument("--find_config_file",action="store_true", help="Prints the folder of the .env config file")

	parser.add_argument("--check_dependencies", action="store_true", help="Will check if chromedriver, tts, and reddit API should be working. Currently under development may come in the future")


	args = parser.parse_args()
	CONFIG = dotenv_values(".env")

	#checking for support flags

	if args.find_config_file: # if someone's using this help utility
		print(os.path.join(os.getcwd(), ".env"))
		quit() # exit program
	
	elif args.check_dependencies:
		print("Currently under development, come back later")
		quit()

	# data validation

	background_path = args.v if args.v != "" else CONFIG['BACKGROUND_VIDEO_PATH']
	if background_path == "": # means that .env and -v are blank
		print("Error: No background path specified via -v or via .env")
		quit()

	audio_provider = args.a if args.a in [0,1,2,3] else -1
	if audio_provider == -1: # not within choices
		print("Error: Invalid -a argument, see --help for more details")
		quit()

	limit = args.l
	if limit <= 0: # must be greater than zero
		print("Error: invalid -l argument, see --help for more details")
		quit()

	save_path = args.p 
	if not os.path.exists(save_path): # Better to throw an error here than later 
		print("Error: Specified path from -p does not exist")
		quit()


	if args.use_text_file: # see --help for more details
		try:
			if args.link == "": # link must exist
				print(f"Path is blank")
				quit()
			# if there is no -v argument, but a config entry				
			with open(args.link, "r") as f:
				for line in f.readlines():
					askReddit(
						line, 
						limit,
						background_path,
						save_path,
						datetime.now().strftime("%Y%m%d-%H%M%S"),
						audio_provider,
						)

		except Exception as e:
			print(f"Error happened with opening {args.link}, try again or check if path is correct")
			quit()

	else: # if it's relying on only links
		askReddit(
				args.link, 
				limit,
				background_path,
				save_path,
				datetime.now().strftime("%Y%m%d-%H%M%S"),		
				audio_provider,		
						)
