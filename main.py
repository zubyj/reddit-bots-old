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

# Creates formatted log.
def create_log(data, comment):
    return {
        "comment":comment.body,
        "reply":data["text"],
        "ratio":data["ratio"],
        "accepted_ratio":data["accepted_ratio"],
        "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "season":data["season"],
        "episode":data["episode"],
        "comment_id":comment.id,
        "line_id":data["id"]
    }

# Writes the reddit comment and bots response to given file.
def log_comment(filename, data, comment):
    with open(filename) as f:
        logs = json.load(f)
    temp = logs["logs"]
    obj = create_log(data, comment)
    temp.append(obj)
    with open(filename, 'w') as f:
        json.dump(logs, f, indent=4)

# Gets line from given id and increments count.
# Function is called when bot replies to a comment.
def increm_reply_count(filename, id):
    with open(filename) as f:
        data = json.load(f)
    lines = data["lines"]
    for line in lines:
        if line["id"] == id:
            count = line["reply_count"] +1
            line["reply_count"] = count
            print(count)
            print(isinstance(count, str))
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
                return

# Given a reddit comment, returns the most identical line
def get_best_match(phrase, lines):
    highestRatio = 0
    for line in lines:
        text = line["line"]
        ratio = fuzz.ratio(phrase, text)
        if ratio >= highestRatio:
            bestLine = line
            highestRatio = ratio

    return {
        "text":bestLine["response"]["text"],
        "ratio":highestRatio,
        "season":bestLine["season"],
        "episode":bestLine["episode"],
        "accepted_ratio":bestLine["accepted_ratio"],
        "id":bestLine["id"]
    }

def show_bot_output(comment, obj):
    print(comment)
    print(obj["text"])
    print(obj["ratio"])
    print()

# Checks stream of new comments and replies to 
# comments that match the minimum ratio specified.
def run_bot(bot_name, lines_file, subreddit="DunderMifflin"):

    # Create instance of reddit account and subreddit.
    reddit = praw.Reddit(bot_name)
    subreddit = reddit.subreddit("DunderMifflin")

    # Open file of character's lines.
    with open(lines_file) as f:
        data = json.load(f)
    lines = data["lines"]

    # Check every new comment and tries to find the closest matching line
    # that the character has responded to.
    #
    # Every match returns a ratio.
    # If the min_ratio is over specified value, the bot will reply to the comment.
    min_ratio = 55
    min_rej_ratio = 45

    for comment in subreddit.stream.comments():
        if (comment.author != bot_name and len(comment.body) >= 20):
            obj = get_best_match(comment.body, lines)
            ratio = obj["ratio"]
            accepted_ratio = int(obj["accepted_ratio"])

            if ratio >= min_ratio or ratio >= accepted_ratio:
                if not is_logged('comment_log.json', comment.id):
                    log_comment('comment_log.json', obj, comment)
                    comment.reply(obj["text"])
                    print("ACCEPTED")
                    increm_reply_count(lines_file, obj["id"])
                    show_bot_output(comment.body, obj)

            elif ratio >= min_rej_ratio and not is_logged('rejected_log.json', comment.id):
                #log_comment('rejected_log.json', obj, comment)
                print("REJECTED")
                show_bot_output(comment.body, obj)

if __name__ == "__main__":
    run_bot('dwight-schrute-bot', 'dwight-replies.json')




