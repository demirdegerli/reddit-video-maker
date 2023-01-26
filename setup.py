import os
from dotenv import load_dotenv
from gtts.langs import _main_langs
import validators

def key_and_value(dictionary):
    dictionary_stringified = ""
    for key, value in dictionary.items():
        dictionary_stringified += "{}: {}\n".format(key, value)
    return dictionary_stringified

load_dotenv()

client_id = False
client_secret = False

comment_length_to_select = 5
subreddit = "AskReddit"
post_scan_limit = 120
character_limit = 240
flair = "" # default is blank / flair name or blank string to flairless search
language = "en" # tts language
background_video_url = "https://www.youtube.com/watch?v=n_Dv4JMiwK8" # video must be longer than 59 seconds
background_video_start = 10 # background video start in seconds / if video actually starts at beginning, enter 0
pick_random = True # default is true / if it's false user will prompted for entering post link

env_prompt = input("""Entering setup. Be sure you have these credentials:
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
        comment_length_to_select_p = input("Comment length to select (press enter with nothing entered to use default): ")
        if comment_length_to_select_p:
            while not comment_length_to_select_p.isdigit():
                if not comment_length_to_select_p:
                    break
                comment_length_to_select_p = input("Comment length to select (press enter with nothing entered to use default): ")
            if comment_length_to_select_p:
                comment_length_to_select = int(comment_length_to_select_p)
        subreddit_p = input("Subreddit (press enter with nothing entered to use default): ")
        if subreddit_p:
            subreddit = subreddit_p
        post_scan_limit_p = input("Post scan limit (how much posts scanned in random instance / press enter with nothing entered to use default): ")
        if post_scan_limit_p:
            while not post_scan_limit_p.isdigit():
                if not post_scan_limit_p:
                    break
                post_scan_limit_p = input("Post scan limit (how much posts scanned in random instance / press enter with nothing entered to use default): ")
            if post_scan_limit_p:
                post_scan_limit = int(post_scan_limit_p)
        character_limit_p = input("Character limit (character limit for texts / press enter with nothing entered to use default): ")
        if character_limit_p:
            while not character_limit_p.isdigit():
                if not character_limit_p:
                    break
                character_limit_p = input("Character limit (character limit for texts / press enter with nothing entered to use default): ")
            if character_limit_p:
                character_limit = int(character_limit_p)
        flair_p = input("Flair (flair name / if there's no flair press enter with nothing entered): ")
        if flair_p:
            flair = flair_p
        if not flair:
            flair = ""
        print(key_and_value(_main_langs()))
        language_p = input("Language (tts language / press enter with nothing entered to use default): ")
        if language_p:
            while language_p not in _main_langs():
                if not language_p:
                    break
                language_p = input("Language (tts language / press enter with nothing entered to use default): ")
            if language_p:
                language = language_p
        background_video_url_p = input("Background video URL (press enter with nothing entered to use default): ")
        if background_video_url_p:
            while not validators.url(background_video_url_p):
                if not background_video_url_p:
                    break
                background_video_url_p = input("Background video URL (press enter with nothing entered to use default): ")
            if background_video_url_p:
                background_video_url = background_video_url_p
        background_video_start_p = input("Background video start (background video actually start time in seconds e.g. 2:20 -> 140 / press enter with nothing entered to use default): ")
        if not background_video_start_p == "":
            while not background_video_start_p.isdigit():
                if background_video_start_p == "":
                    break
                background_video_start_p = input("Background video start (actual start time of background video in seconds e.g. 2:20 -> 140 / press enter with nothing entered to use default): ")
            if not background_video_start_p == "":
                background_video_start = background_video_start_p
        pick_random_p = input("Pick random (random post or entered post link) (yes/no/press enter with nothing entered to use default): ").lower()
        if pick_random_p == "yes":
            pick_random = True
        elif not pick_random_p:
            pass
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
    env.close()
    continue_prompt = input("Settings are successfully configured. Continue as normal? (yes/no) > ")
    if continue_prompt == "yes":
        os.system("python3 main.py")
        quit()
    else:
        print("Quiting...")
        quit()
else:
    print("Quiting...")
    quit()
