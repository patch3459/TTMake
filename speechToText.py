from fileinput import filename
import os
import re
import requests as r
from requests.exceptions import JSONDecodeError
from moviepy.audio.AudioClip import concatenate_audioclips, CompositeAudioClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from requests.exceptions import JSONDecodeError
import time
import shutil

def makeAudio(paragraphs, dirr, audio_code):


        if audio_code == 0:

                url = "https://streamlabs.com/polly/speak"

                for index, p in enumerate(paragraphs):

                        params = {
                                "voice" : "Matthew",
                                "text"  : p.replace("&", "and"),
                                "service": "polly"}

                        response = r.post(url, data=params)
                        filename = f"audio{index+1}.mp3"

                        try:
                                resp = r.post(url, params=params)
                                voice_data = r.get(resp.json()["speak_url"])

                                with open(os.path.join(dirr, filename), "wb") as f:
                                        f.write(voice_data.content)

                        except:
                                if response.json()["error"] == "Text length is too long!":

                                        clips = []

                                        chunkId = 0

                                        chunks = [m.group().strip() for m in re.finditer(r" *((.{0,499})(\.|.$))", p)]

                                        if not os.path.isdir(os.path.join(dirr,"tmp")):
                                                os.mkdir(os.path.join(dirr, "tmp"))

                                        for i, item in enumerate(chunks):
                                                body = {"voice": "Matthew", "text": item, "service": "polly"}
                                                resp =  r.post(url, data=body)
                                                #print(resp.json())
                                                try: 
                                                        voice_data = r.get(resp.json()["speak_url"])
                                                except:
                                                        continue

                                                with open(os.path.join(dirr,"tmp",f"audio{index + 1}.mp3").replace(".mp3", f"-{chunkId}.mp3"),"wb" ) as f :

                                                        f.write(voice_data.content)
        
                                                clips.append(os.path.join(dirr, "tmp" ,filename).replace(".mp3", f"-{chunkId}.mp3"))

                                                chunkId += 1


                                        if len(clips) > 1:
                                                clipConcatenate = [AudioFileClip(c) for c in clips]
                                                final_clip = concatenate_audioclips(clipConcatenate)
                                                final_clip.write_audiofile(os.path.join(dirr,filename))
                                        else:
                                                os.rename(clips[0], os.path.join(dirr,filename))  

        elif audio_code == 1:
                        # shutil.rmtree(os.path.join(dirr, "tmp"))
                        import azure.cognitiveservices.speech as speechsdk

                        speech_config = speechsdk.SpeechConfig(subscription="", region="eastus")
                        #language
                        speech_config.speech_synthesis_voice_name='en-US-JacobNeural'

                        for index, p in enumerate(paragraphs):
                                audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True, filename= os.path.join(dirr, f"audio{index}.wav"))

                                speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

                                result = speech_synthesizer.speak_text_async(p).get()


        elif audio_code == 2:
                for index, p in enumerate(paragraphs):
                        tts = gTTS(p, lang="en", tld="co.uk")
                        tts.save(
                                os.path.join(dirr,f"audio{index}.mp3")
                        )


        elif audio_code == 3:
                #Using the utility balabolka
                #http://www.cross-plus-a.com/bconsole.htm

                #You'll have to install the CLI locally, ymmv but the command should work on everything
                
                for index, paragraph in enumerate(paragraphs):
                        
                        path = os.path.join(dirr, f"audio{index}.wav")
                        paragraph = paragraph.replace("\n", ". ").replace("\"", "") # the newlines will kill the command
                        command = f"balcon -t \"{paragraph}\" -n David -w {path} -p -10 --voice1-rate 1.5"
                        os.system(command)


