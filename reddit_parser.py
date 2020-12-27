import praw
import json
from word_matcher import get_best_match
from datetime import datetime

def log_comment(filename, data):
    with open(filename, 'w') as f:
        logs = json.load(f)

reddit = praw.Reddit("dwight-schrute-bot")
subreddit = reddit.subreddit("DunderMifflin")

with open('line-replies2.json') as f:
    data = json.load(f)
lines = data["lines"]


for comment in subreddit.stream.comments():
    obj = get_best_match(comment.body, lines)
    if obj["ratio"] > 70:
        obj2 = {
            "comment":comment.body,
            "reply":obj["text"],
            "ratio":obj["ratio"],
            "time":datetime.now().time()
        }
        with open('comment_log.json') as f2:
            logs = json.load(f2)
            temp = logs["logs"]
            temp.append(obj2)
        with open('comment_log.json', 'w') as f3:
            json.dump(logs, f3, indent=4)
        print(obj2)