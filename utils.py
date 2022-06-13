import re
from unidecode import unidecode as normalize
from praw.models import MoreComments
import os

# settings #
from dotenv import load_dotenv
load_dotenv()
character_limit = int(os.getenv("CHARACTER_LIMIT"))

# declare regexs
invalid_regex = "(u\/[^\s]([^\s]+)?)|(\[(removed|deleted)\])|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/\/=]*))|(\[.*\]\(.*\))|(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])"
invalid_regex_control = re.compile(invalid_regex)
multi_line_break_regex = "\n+"
multi_space_regex = " +"

def convert_snake_case(string):
    converted = string.lower()
    converted = re.sub(invalid_regex, "", converted)
    converted = re.sub("[^\w\s]", "", converted).strip()
    converted = "_".join(re.split("\s", converted))
    converted = normalize(converted)
    return converted

def create_tags(string):
    tags = []
    string = string.lower()
    string = re.sub(invalid_regex, "", string)
    string = re.sub("[^\w\s]", "", string).strip()
    tags = re.split("\s", string)
    tags = list(filter(None, tags))
    return tags

# get content from the comment object
def get_comment_content(comment):
    return comment.body

# control if post contains only text
def is_self(post):
    result = False
    if post.is_self:
        result = True
    return result

# remove comments that's character length longer than provided character limit
def control_character_length(string):
    result = False
    if len(string) > character_limit:
        result = True
    return result

# remove duplicate comments, MoreComments objects and pinned comments
def clean_comments(comments):
    seen_comment_contents = []
    duplicates_removed = []
    for comment in comments:
        if not isinstance(comment, MoreComments):
            if comment.body not in seen_comment_contents and not comment.stickied:
                duplicates_removed.append(comment)
                seen_comment_contents.append(comment.body)
    return duplicates_removed

# print summary
def summary(post, focused_comments):
    dashes = ""
    for dash in range(os.get_terminal_size().columns):
        dashes += "-"

    list_number = 0
    list_items = []
    for comment in focused_comments:
        list_number+=1
        # clear the invalids
        clear_comment = re.sub(invalid_regex, '', comment.body)
        author = "[deleted]"
        if comment.author:
            author = comment.author.name
        clear_comment += " ~ by u/" + author
        list_items.append("{}- {}".format(list_number, clear_comment.strip()))

    # make the list actually a string
    stringified = "\n".join(list_items)
    list_number = 0

    author = "[deleted]"
    if post.author:
        author = post.author.name

    print("""
Top comments of post named "{}" by u/{}
{}
{}
{}
{}
    """.format(post.title, author, dashes, (post.selftext or "< no content >"), dashes, stringified))
