import json
import praw
from main import get_best_match

reddit = praw.Reddit("dwight-schrute-bot")
subreddit = reddit.subreddit("DunderMifflin")

with open("dwight/replies.json") as f:
    data = json.load(f)
lines = data["lines"]

for line in lines:
    del line["accepted_ratio"]

with open('test.json', 'w') as f:
    json.dump(data, f, indent=4)