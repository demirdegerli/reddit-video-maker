from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, CompositeAudioClip, ImageClip
from gtts import gTTS
from gtts.langs import _main_langs
from random import randint as get_random
import os
from glob import glob
from moviepy.config import IMAGEMAGICK_BINARY
#-------------------------------------------------------------------------------------------------------------#
from utils import *

# settings #
from dotenv import load_dotenv
load_dotenv()
language = os.getenv("TTS_LANGUAGE")
background_video_start = int(os.getenv("BACKGROUND_VIDEO_START"))

def render_video(focused_comments, post):
    global language, background_video_start, text_number
    comments = []
    # prepare comments for video
    for comment in focused_comments:
        author = "[deleted]"
        if comment.author:
            author = comment.author.name
        body = re.sub(multi_line_break_regex, '\n', comment.body)
        body = re.sub(multi_space_regex, ' ', body)
        body = re.sub(invalid_regex, '', body)
        comments.append({
            "text": body,
            "author": "u/"+author
        })

    if language:
        if language not in _main_langs():
            language = "en"
    else:
        language = "en"

    def create_audio(content, filename, start):
        audio_obj = gTTS(text=content, lang=language, slow=False)
        audio_obj.save("assets/temp/{}.mp3".format(filename))
        return AudioFileClip("assets/temp/{}.mp3".format(filename)).set_start(start)

    text_number = 1
    def create_text(content, fontsize, start, duration):
        textclip = None
        try:
            textclip = TextClip(content, font='Tahoma', fontsize=fontsize+30, method='caption', color='white', interline=True, stroke_color='black', stroke_width=2).set_position('center').subclip(0, duration).set_start(start)
        except Exception as e:
            global text_number
            print(e)
            print("Text couldn't be created using the `caption` method. Trying again using the `pango` method. You can see the error above.")
            txt = open('assets/temp/text_{}.txt'.format(text_number), 'w')
            txt.write(content)
            txt.close()
            os.system("{} -define pango:markup=false -background transparent -fill white -font Tahoma -bordercolor none -border 2 -channel A -blur 2x2 -level 0,0% -pointsize {} -size 1070x -gravity center -interline-spacing 1 pango:@assets/temp/text_{}.txt -type truecolormatte PNG32:assets/temp/text_{}.png".format(IMAGEMAGICK_BINARY, fontsize, text_number, text_number))
            textclip = ImageClip('assets/temp/text_{}.png'.format(text_number)).set_position('center').subclip(0, duration).set_start(start)
            text_number += 1
        return textclip

    waits_duration = 1

    audios = [
        create_audio(post.title, "audio_title", 0),
    ]
    comment_number = 1
    if post.selftext:
        audios.append(create_audio(post.selftext, "audio_selftext", audios[0].duration+1))
        waits_duration += 1
        comment_number += 1

    audio_duration = 0
    for audio in audios:
        audio_duration += audio.duration

    with_audio_comments = []
    for comment in comments:
        audio_duration = 0
        for audio in audios:
            audio_duration += audio.duration
        audio = create_audio(comment["text"], "audio_{}".format(comment_number), audio_duration+1)
        if not (audio_duration + audio.duration > (59-waits_duration)):
            with_audio_comments.append(comment)
            audios.append(audio)
            waits_duration += 1
            comment_number += 1
    comments = with_audio_comments

    audio_duration = 0
    for audio in audios:
        audio_duration += audio.duration

    # video
    VideoFileClip.reW = lambda clip: clip.resize(width=1080)
    VideoFileClip.reH = lambda clip: clip.resize(width=1920)

    if not background_video_start:
        background_video_start = 0
    background = VideoFileClip("assets/background.mp4")
    if background.duration - background_video_start < 59:
        print("Background video must be 59 seconds or longer. If video 59 seconds or longer, try decreasing background video start.")
        print("Quiting...")
        quit()
    random_start = get_random(background_video_start, (round(background.duration-background_video_start)-(round(audio_duration)+1)))
    clip = (
    background.subclip(random_start, random_start+round(audio_duration)+1+1)
    .without_audio()
    .resize(height=1920)
    .crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    )

    will_nested = [clip]

    will_nested.append(create_text("{}\n\nu/{}\nr/{}".format(post.title, author, post.subreddit.display_name), 75, 0, audios[0].duration))

    comment_number = 1
    audio_number = 0

    audio_duration = audios[0].duration

    if post.selftext:
        will_nested.append(create_text(post.selftext, 55, audios[0].duration+1, audios[1].duration))
        comment_number += 1
        audio_number += 1
        audio_duration += audios[1].duration

    comment_index = 0
    for _ in audios[comment_number::]:
        text = create_text("{}\n\n{}".format(comments[comment_index]["text"], comments[comment_index]["author"]), 55, audio_duration+1, audios[comment_number].duration)
        will_nested.append(text)
        audio_duration += audios[comment_number].duration
        comment_number += 1
        audio_number += 1
        comment_index += 1

    nested_audio = CompositeAudioClip(audios)

    # export
    result = CompositeVideoClip(will_nested).set_audio(nested_audio)
    print("Video duration: {} seconds".format(round(result.duration)))
    filename = convert_snake_case(post.title)
    result.write_videofile("outputs/{}.mp4".format(filename))

    for file in glob("assets/temp/audio*"):
        os.remove(file)
    for file in glob("assets/temp/text*"):
        os.remove(file)
