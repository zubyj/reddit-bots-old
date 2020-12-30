import praw
import json
from fuzzywuzzy import fuzz
from datetime import datetime
import time

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
    season = ""
    episode = ""
    for line in lines:
        text = line["line"]

        ratio = fuzz.ratio(phrase, text)
        if ratio > highestRatio:
            highestRatio = ratio
            bestQuote = line["response"]["text"]
            season = line["season"]
            episode = line["episode"]

    obj = {
        "text":bestQuote,
        "ratio":highestRatio,
        "season":season,
        "episode":episode
    }
    return obj

# Checks stream of new comments and replies to 
# comments that match the minimum ratio (min_ratio) specified.
def run_bot(bot_name, lines_file, subreddit="DunderMifflin"):
    # Create instance of reddit account
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit("DunderMifflin")
    # Open file of character's lines.
    with open(lines_file) as f:
        data = json.load(f)
    lines = data["lines"]
    min_ratio = 48
    min_rej_ratio = 40
    for comment in subreddit.stream.comments():
        if (comment.author != bot_name and len(comment.body) > 20):
            obj = get_best_match(comment.body, lines)
            if obj["ratio"] >= min_ratio and not is_logged('comment_log.json', comment.id):
                log_comment('comment_log.json', obj, comment)
                comment.reply(obj["text"])
                time.sleep(60)
            elif obj["ratio"] >= min_rej_ratio and not is_logged('rejected_log.json', comment.id):
                log_comment('rejected_log.json', obj, comment)

if __name__ == "__main__":
    run_bot('dwight-schrute-bot', 'dwight-replies3.json')




