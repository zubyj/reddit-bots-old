import praw
import json
from word_matcher import get_best_match

reddit = praw.Reddit("dwight-schrute-bot")
subreddit = reddit.subreddit("DunderMifflin")

with open('line-replies2.json') as f:
    data = json.load(f)
lines = data["lines"]

for comment in subreddit.stream.comments():
    obj = get_best_match(comment.body, lines)
    if obj["ratio"] > 80:
        print(comment.body)
        print(obj)
