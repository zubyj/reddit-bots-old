import json
import praw

reddit = praw.Reddit("dwight-schrute-bot")

for submission in reddit.subreddit('all').rising(limit=15):
    submission.comments.replace_more(limit=None)
    print(submission.subreddit.display_name)
    if not submission.over_18:
        for comment in submission.comments.list():
            print()