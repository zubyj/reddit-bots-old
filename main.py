import praw
import json
from fuzzywuzzy import fuzz
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

# Creates formatted log object.
def create_log(data, comment):
    return {
        "comment":comment.body,
        "reply":data["text"],
        "ratio":data["ratio"],
        "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "season":data["season"],
        "episode":data["episode"],
        "comment_id":comment.id
    }

# Adds comments and responses to given json file.
def log_comment(filename, data, comment):
    with open(filename) as f:
        logs = json.load(f)
    temp = logs["logs"]
    obj = create_log(data, comment)
    temp.append(obj)
    with open(filename, 'w') as f:
        json.dump(logs, f, indent=4)

# Gets best reply to given phrase.
def get_best_match(phrase, lines):
    highestRatio = 0
    bestQuote = ""
    for line in lines:
        text = line["line"]
        ratio = fuzz.ratio(phrase, text)
        if ratio > highestRatio:
            highestRatio = ratio
            bestQuote = line["response"]["text"]
    obj = {
        "text":bestQuote,
        "ratio":highestRatio,
        "season":line["season"],
        "episode":line["episode"]
    }
    return obj

def run_bot(bot_name, subreddit="DunderMifflin"):
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit("DunderMifflin")
    with open('dwight_replies2.json') as f:
        data = json.load(f)
    lines = data["lines"]
    min_ratio = 70
    min_bad_ratio = 55
    for comment in subreddit.stream.comments():
        if (comment.author != bot_name and len(comment.body) > 20):
            obj = get_best_match(comment.body, lines)
            if obj["ratio"] > min_ratio and not is_logged('comment_log.json', comment.id):
                log_comment('comment_log.json', obj, comment)
                comment.reply(obj["text"])
                print("Comment : " + comment.body)
                print("Response : " + obj["text"])
                print()
            elif obj["ratio"] > min_bad_ratio and not is_logged('rejected_log.json', comment.id):
                log_comment('rejected_log.json', obj, comment)
                print("Comment : " + comment.body)
                print("Response : " + obj["text"])
                print()

if __name__ == "__main__":
    run_bot('dwight-schrute-bot')




