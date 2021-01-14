import json
import praw

reddit = praw.Reddit("andy-bernard-bot")
subreddit = reddit.subreddit("DunderMifflin")

for comment in subreddit.stream.comments():
    print(comment.body)