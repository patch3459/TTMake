# TTMake - a utility for generating AskReddit Style Tiktok Videos

 Interested in creating your own AskReddit videos with only a link? Well this progam uses just Python to create these magical videos. 

## Motivation 

I come from a background in creating TikTok videos whether it's in fittness, education, or even gaming. I noticed the video genre appear and decided to make my own utility in house to run my own channel. I ran it for a few weeks and you can find the results in this channel [here](https://tiktok.com/@hot_reddit_stories).

Unlike the other predominating program that creates this video type, TTMake uses Selenium to power its image processing and supports Microsoft Azure TTS, Balbonka, google translate TTS. 

## Requirements

* Python3.8 or higher
* FFMPEG
* Chromedriver 
* MoviePy and other packages in requirements.txt
* Reddit Account with access to praw 


## Setup

I don't recomend using setup.py or trying to install this project via pip. There are just many errors and I think you'd be better off having this locally cloned on your machine.

Step 1: Clone the repository
```
$ git clone https://github.com/patch3459/TT_Autom8.git
```

Step 2: Install dependencies via pip
```
$ python3 -m pip install -r requirements.txt
```

Step 3: Enter folder
```
$ cd TT_Autom8
```

Step 4: Run the ttMake command
```
$ python3 ttMake.py ....
```

If you're ever confused in regards to options and arguments type in
```
$ python3 ttMake.py --help
```

## Disclaimer

There are some bugs in this program. Due to the nature of the Selenium implementation, there can be some unexpected behaviour with screenshots. There also may be issues with praw and psaw retrieving content from deleted or really old posts. I do not assume any responsibility for any damage that occurs due to using this program. Use this at your own risk. 

Additionally, I am aware that as time goes by, there may appear new bugs and errors I am not aware of. Because I'm a college student I'm probably not going to be able to always fix it. I encourage you to modify the code and make changes as necessary. Within the renderReddit.py file there are other functions I've written that haven't been implemented into the CLI. Fork the project, make major changes, 
this project is under an MIT license.


## Closing Notes

I just want to thank my parents, my friends, and god for helping me get through tough times and finally be able to make software that I'm proud of. I want to thank you for reading this, god bless you, good luck, stay safe, and enjoy!

