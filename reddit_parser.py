import praw
import json
from word_matcher import get_best_match
from datetime import datetime

def log_comment(filename, data):
    with open(filename, 'w') as f:
        logs = json.load(f)

def is_logged(filename, comment_id):
    with open(filename) as f:
        logs = json.load(f)
        # Gets logs object
        logs = logs["logs"]
        for log in logs:
            if (log["comment_id"] == comment_id):
                return True
        return False


reddit = praw.Reddit("dwight-schrute-bot")
subreddit = reddit.subreddit("DunderMifflin")

with open('line-replies2.json') as f:
    data = json.load(f)
lines = data["lines"]


for comment in subreddit.stream.comments():
    obj = get_best_match(comment.body, lines)
    if obj["ratio"] > 70 and not is_logged('comment_log.json', comment.id):
        obj2 = {
            "comment":comment.body,
            "reply":obj["text"],
            "ratio":obj["ratio"],
            "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "comment_id":comment.id
        }
        with open('comment_log.json') as f2:
            logs = json.load(f2)
            temp = logs["logs"]
            temp.append(obj2)
        with open('comment_log.json', 'w') as f3:
            json.dump(logs, f3, indent=4)
        print(obj2)