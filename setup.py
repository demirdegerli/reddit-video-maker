import os
from dotenv import load_dotenv

load_dotenv()

client_id = False
client_secret = False

comment_length_to_select = 5
subreddit = "AskReddit"
post_scan_limit = 120
character_limit = 240
flair = False # default is false / flair name or false to flairless search
language = "en" # tts language
background_video_url = "https://www.youtube.com/watch?v=n_Dv4JMiwK8" # video must be longer than 59 seconds
background_video_start = 10 # background video start in seconds / if video actually starts at beginning, enter 0
pick_random = True # default is true / if it's false user will prompted for entering post link

env_prompt = input(""".env file invalid or does not exists. Be sure you have these credentials:
Client ID
Client Secret
Comment length to select
Subreddit
Post scan limit (how much posts scanned in random instance)
Character limit (character limit for texts)
Flair
Language (tts language)
Background video URL
Background video start (background video actually start time)
Pick random (random post or entered post link)
Continue? (yes/no) > """).lower()
if env_prompt == "yes":
    default_prompt = input("Use default settings? (yes/no) > ").lower()
    if default_prompt == "yes":
        print("Using default settings but these credentials must be entered manually.\n- Client ID\n- Client Secret")
        client_id = input("Client ID: ")
        while not client_id:
            client_id = input("Client ID: ")
        client_secret = input("Client Secret: ")
        while not client_secret:
            client_secret = input("Client Secret: ")
    elif default_prompt == "no":
        client_id = input("Client ID: ")
        while not client_id:
            client_id = input("Client ID: ")
        client_secret = input("Client Secret: ")
        while not client_secret:
            client_secret = input("Client Secret: ")
        comment_length_to_select = input("Comment length to select: ")
        while not comment_length_to_select.isdigit():
            comment_length_to_select = input("Comment length to select: ")
        comment_length_to_select = int(comment_length_to_select)
        subreddit = input("Subreddit: ")
        while not subreddit:
            subreddit = input("Subreddit: ")
        post_scan_limit = input("Post scan limit (how much posts scanned in random instance): ")
        while not post_scan_limit.isdigit():
            post_scan_limit = input("Post scan limit (how much posts scanned in random instance): ")
        post_scan_limit = int(post_scan_limit)
        character_limit = input("Character limit (character limit for texts): ")
        while not character_limit.isdigit():
            character_limit = input("Character limit (character limit for texts): ")
        character_limit = int(character_limit)
        flair = input("Flair (flair name / if there's no flair, type \"there is no flair\" without quotes): ")
        while not flair:
            flair = input("Flair: ")
        if flair.lower() == "there is no flair":
            flair = False
        language = input("Language (tts language): ")
        while not language:
            language = input("Language (tts language): ")
        background_video_url = input("Background video URL: ")
        while not background_video_url:
            background_video_url = input("Background video URL: ")
        background_video_start = input("Background video start (background video actually start time): ")
        while not background_video_start.isdigit():
            background_video_start = input("Background video start (background video actually start time): ")
        background_video_start = int(background_video_start)
        pick_random = input("Pick random (random post or entered post link) (yes/no): ").lower()
        while not pick_random == "yes" or pick_random == "no":
            pick_random = input("Pick random (random post or entered post link): ")
        if pick_random == "yes":
            pick_random = True
        else:
            pick_random = False
    else:
        print("Quiting...")
        quit()
    env = open(".env", "w")
    env.write("""
REDDIT_CLIENT_ID="{}"
REDDIT_CLIENT_SECRET="{}"
COMMENT_LENGTH_TO_SELECT={}
SUBREDDIT="{}"
POST_SCAN_LIMIT={}
CHARACTER_LIMIT={}
FLAIR="{}"
TTS_LANGUAGE="{}"
BACKGROUND_VIDEO_URL="{}"
BACKGROUND_VIDEO_START={}
PICK_RANDOM={}
""".format(client_id, client_secret, comment_length_to_select, subreddit, post_scan_limit, character_limit, flair, language, background_video_url, background_video_start, pick_random))
    continue_prompt = input("Settings are succesfully configured. Continue as normal? (yes/no) > ")
    if continue_prompt == "yes":
        os.system("python3 main.py")
    else:
        print("Quiting...")
        quit()
else:
    print("Quiting...")
    quit()