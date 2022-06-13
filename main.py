import os
from glob import glob
from pytube import YouTube as youtube
from dotenv import load_dotenv
#--------------------------------------------------------#

# environment variables #
load_dotenv()
setting_keys = [
    "REDDIT_CLIENT_ID",
    "REDDIT_CLIENT_SECRET",
    "COMMENT_LENGTH_TO_SELECT",
    "SUBREDDIT",
    "POST_SCAN_LIMIT",
    "CHARACTER_LIMIT",
    "FLAIR",
    "TTS_LANGUAGE",
    "BACKGROUND_VIDEO_URL",
    "BACKGROUND_VIDEO_START",
    "PICK_RANDOM"
]
settings_valid = True
for key in setting_keys:
    if key not in os.environ:
        settings_valid = False
if not os.path.exists(".env") or not settings_valid:
    setup_prompt = input(".env file invalid or does not exists. Enter setup? (yes/no) > ")
    if setup_prompt == "yes":
        os.system("python3 setup.py")
        quit()
    else:
        print("Quiting...")
        quit()

background_video_url = os.getenv("BACKGROUND_VIDEO_URL")
pick_random = os.getenv("PICK_RANDOM")
if pick_random == "True":
    pick_random = True
else:
    pick_random = False

from utils import *
from reddit import get_comments, reddit_instance
from video import render_video


paths = ["assets", "assets/temp", "outputs"]

for path in paths:
    if not os.path.exists(path):
        os.makedirs(path)

for file in glob("assets/temp/audio*"):
    os.remove(file)

if not os.path.exists("assets/background.mp4"):
    print("Background video not found, downloading background video. This is an one-time process and might take a while.")
    youtube_video = youtube(background_video_url).streams.filter(fps=60, res="1080p", mime_type="video/mp4", only_video=True).first()
    youtube_video_filesize = youtube_video.filesize/1048576
    if youtube_video_filesize > 1024:
        youtube_video_filesize = "{} {}".format(round(youtube_video_filesize/1024, 1), "GB")
    else:
        youtube_video_filesize = "{} {}".format(round(youtube_video_filesize, 1), "MB")
    print("Video size: " + youtube_video_filesize)
    print("Downloading...")
    youtube_video.download("assets", "background.mp4")
    print("Background video downloaded. Continuing as normal.")

post = focused_comments = False

if pick_random:
    post, focused_comments = reddit_instance()
else:
    post, focused_comments = get_comments()

if post == False and focused_comments == False:
    print("Quiting...")
    quit()

render_video(focused_comments, post)