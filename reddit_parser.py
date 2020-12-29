import praw
import json
from word_matcher import get_best_match
from datetime import datetime

# Checks if bot already replied to comment
def is_logged(filename, comment_id):
    with open(filename) as f:
        data = json.load(f)
    logs = data["logs"]
    for log in logs:
        if log["comment_id"] == comment_id:
            return True
    return False

# Creates a formatted log from comment and reply
def create_log(data, comment):
    return {
        "comment":comment.body,
        "reply":data["text"],
        "ratio":data["ratio"],
        "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "comment_id":comment.id
    }

# Creates a log and updates json file specified.
def log_comment(filename, data, comment):
    with open(filename) as f:
        logs = json.load(f)
    temp = logs["logs"]
    obj = create_log(data, comment)
    temp.append(obj)
    with open(filename, 'w') as f:
        json.dump(logs, f, indent=4)

reddit = praw.Reddit("dwight-schrute-bot")
subreddit = reddit.subreddit("DunderMifflin")

with open('line-replies2.json') as f:
    data = json.load(f)
lines = data["lines"]

for comment in subreddit.stream.comments():
    if (comment.author != "dwight-schrute-bot" and len(comment.body) > 20):
        obj = get_best_match(comment.body, lines)
        if obj["ratio"] > 60 and not is_logged('comment_log.json', comment.id):
            log_comment('comment_log.json', obj, comment)
            comment.reply(obj["text"])
        elif obj["ratio"] > 50 and not is_logged('rejected_log.json', comment.id):
            log_comment('rejected_log.json', obj, comment)