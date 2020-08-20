# Imports
import praw
import json
import pygame
import io
import time
from gtts import gTTS 
import re
from mutagen.mp3 import MP3

# Start pygame sound engine
pygame.mixer.init()

# Function To Play Audio given text
def play_audio(text):
    tts = gTTS(text=text, lang='en') 
    audio_bytes_object = io.BytesIO()
    tts.write_to_fp(audio_bytes_object)
    audio_length = MP3(audio_bytes_object).info.length
    audio_bytes_object.seek(0)
    pygame.mixer.music.load(audio_bytes_object)
    pygame.mixer.music.play()
    time.sleep(audio_length + 1)

# Removes Links & Some Special Characters from text
def filter_text(text):
    text = re.sub(r'(https?:\/\/)?(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', '', text, flags=re.MULTILINE)
    return re.sub(r'[\]\[\(\)]', '', text, flags=re.MULTILINE)

# Loads Settings
with open("reddit_details.json", 'r') as i:
    settings = json.loads(i.read())

# Creates Reddit object to read submissions
reddit = praw.Reddit(client_id=settings['client_id'],
                     client_secret=settings['client_secret'],
                     user_agent=settings['user_agent'],
                     username=settings['username'],
                     password=settings['password'])

# Creates a stream of new content from r/conspiracy
for submission in reddit.subreddit("conspiracy").stream.submissions(skip_existing=False):
    if submission.is_self: # Checks to see if text only post
        full_text = submission.title + " " + submission.selftext # Combines title and body into a single string
        play_audio(filter_text(full_text)) # Plays Audio