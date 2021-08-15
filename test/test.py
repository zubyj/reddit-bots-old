import json
import praw
from main import get_best_match

reddit = praw.Reddit("dwight-schrute-bot")

for submission in reddit.subreddit('all').rising(limit=15):
    submission.comments.replace_more(limit=None)
    if not submission.over_18:
        for comment in submission.comments.list():
            print(comment)