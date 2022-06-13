import praw
import re
import os
import validators
from dotenv import load_dotenv
#----------------------------------------------#
from random import randint as get_random
from utils import *

def reddit_instance():
    # settings #
    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    subreddit = os.getenv('SUBREDDIT')
    flair = os.getenv('FLAIR')
    if flair == "False":
        flair = False
    post_scan_limit = int(os.getenv('POST_SCAN_LIMIT'))
    comment_length_to_select = int(os.getenv('COMMENT_LENGTH_TO_SELECT'))
    # setting fixes
    subreddit = re.sub('r\/', '', subreddit)

    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent="comment explorer",
    )

    print("Searching for a random post...")
    results = list(filter(is_self, list(reddit.subreddit(subreddit).hot(limit=post_scan_limit))))
    if flair:
        results = list(filter(is_self, reddit.subreddit(subreddit).search('flair:"{}"'.format(flair), limit=post_scan_limit)))
    random = get_random(0, len(results)-1)
    post = results[random]
    comments_of_post = list(post.comments.replace_more(limit=0))

    comments_of_post = clean_comments(comments_of_post)

    focused_comments = comments_of_post[0:comment_length_to_select]

    character_exceed_length = len(list(filter(control_character_length, list(map(get_comment_content, focused_comments)))))

    # recreate the comments array if array length less than given length and post selftext longer than provided character limit
    invalid_comments_length = len(list(filter(invalid_regex_control.match, list(map(get_comment_content, comments_of_post)))))
    post_selftext_character_control = False
    if post.selftext:
        post_selftext_character_control = control_character_length(post.selftext)
    while (len(comments_of_post) < comment_length_to_select + invalid_comments_length + character_exceed_length) or post_selftext_character_control:
        random = get_random(0, len(results)-1)
        post = results[random]
        comments_of_post = list(post.comments)

        comments_of_post = clean_comments(comments_of_post)

        focused_comments = comments_of_post[0:comment_length_to_select]
        if post.selftext:
            post_selftext_character_control = control_character_length(post.selftext)
        else:
            post_selftext_character_control = False

    # remove invalid and that's character length longer than provided character limit comments
    to_control_comments = list(map(get_comment_content, focused_comments))
    invalid_comments_length = len(list(filter(invalid_regex_control.match, to_control_comments)))
    while invalid_comments_length != 0 or character_exceed_length != 0:
        continuous_comment_position = len(focused_comments)
        current_position = 0
        for comment in focused_comments:
            # remove invalid content
            cleaned = re.sub(invalid_regex, '', comment.body)
            # remove spaces for control
            cleaned = re.sub('[\s]', '', cleaned)
            # control if string is empty
            if cleaned == "" or control_character_length(comment.body):
                focused_comments.pop(current_position)
                focused_comments.append(comments_of_post[continuous_comment_position])
                invalid_comments_length-=1
                continuous_comment_position+=1
            current_position+=1
        # update invalid comments
        to_control_comments = list(map(get_comment_content, focused_comments))
        invalid_comments_length = len(list(filter(invalid_regex_control.match, to_control_comments)))
        # update character exceed length
        character_exceed_length = len(list(filter(control_character_length, list(map(get_comment_content, focused_comments)))))


    # print summary
    summary(post, focused_comments)

    # returning data
    return post, focused_comments


def get_comments():
    # settings #
    load_dotenv()
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    comment_length_to_select = int(os.getenv('COMMENT_LENGTH_TO_SELECT'))

    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent="comment explorer",
    )

    post_url = input("Enter post url: ")
    post = False
    while not validators.url(post_url):
        post_url = input("Enter post url: ")
    while not post:
        try:
            post = reddit.submission(url=post_url)
        except:
            post_url = input("Enter post url: ")
    comments_of_post = post.comments
    comments_of_post = clean_comments(comments_of_post)
    focused_comments = comments_of_post[0:comment_length_to_select]

    character_exceed_length = len(list(filter(control_character_length, list(map(get_comment_content, focused_comments)))))

    post_selftext_character_control = False
    if post.selftext:
        post_selftext_character_control = control_character_length(post.selftext)
    else:
        post_selftext_character_control = False

    invalid_comments_length = len(list(filter(invalid_regex_control.match, list(map(get_comment_content, comments_of_post)))))

    if (len(comments_of_post) < comment_length_to_select + invalid_comments_length + character_exceed_length) or post_selftext_character_control:
        warn_prompt = input("The post you entered does not meet the requirements. Continue anyway? (yes/no) > ")
        if warn_prompt.lower() == "yes":
            warn_prompt = False
        else:
            warn_prompt = True
        if warn_prompt:
            post = focused_comments = False
            return post, focused_comments

    # remove invalid and that's character length longer than provided character limit comments
    to_control_comments = list(map(get_comment_content, focused_comments))
    while invalid_comments_length != 0 or character_exceed_length != 0:
        continuous_comment_position = len(focused_comments)
        current_position = 0
        for comment in focused_comments:
            # remove invalid content
            cleaned = re.sub(invalid_regex, '', comment.body)
            # remove spaces for control
            cleaned = re.sub('[\s]', '', cleaned)
            # control if string is empty
            if cleaned == "" or control_character_length(comment.body):
                focused_comments.pop(current_position)
                focused_comments.append(comments_of_post[continuous_comment_position])
                invalid_comments_length-=1
                continuous_comment_position+=1
            current_position+=1
        # update invalid comments
        to_control_comments = list(map(get_comment_content, focused_comments))
        invalid_comments_length = len(list(filter(invalid_regex_control.match, to_control_comments)))
        # update character exceed length
        character_exceed_length = len(list(filter(control_character_length, list(map(get_comment_content, focused_comments)))))

    
    # print summary
    summary(post, focused_comments)

    # returning data
    return post, focused_comments