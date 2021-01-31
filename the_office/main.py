import praw
import json
from fuzzywuzzy import fuzz
from datetime import datetime
from datetime import time
from bot import bot

# Checks comment logs so bot doesn't reply to same comment.
def is_logged(filename, comment_id):
    with open(filename) as f:
        data = json.load(f)
    logs = data["logs"]
    for log in logs:
        if log["comment_id"] == comment_id:
            return True
    return False

# Writes reddit comment and bots response to given file.
def log_comment(filename, data, comment):
    with open(filename) as f:
        logs = json.load(f)
    temp = logs["logs"]
    obj = {
        "comment":comment.body,
        "reply":data["text"],
        "ratio":data["ratio"],
        "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "season":data["season"],
        "episode":data["episode"],
        "comment_id":comment.id,
        "line_id":data["id"]
    }
    temp.append(obj)
    with open(filename, 'w') as f:
        json.dump(logs, f, indent=4)

# Function is called when bot replies to a comment.
# Increments the reply_count of line from given id.
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
#   that the character has responded to.
def get_best_match(comment, lines):
    highestRatio = 0
    bestLine = lines[0]
    for line in lines:
        text = line["line"]
        ratio = fuzz.ratio(comment, text)
        if ratio >= highestRatio:
            bestLine = line
            highestRatio = ratio
    return {
        "text":bestLine["response"]["text"],
        "ratio":highestRatio,
        "season":bestLine["season"],
        "episode":bestLine["episode"],
        "id":bestLine["id"]
    }

# Makes sure every few comments are unique.
def is_unique_comment(filename, line_id):
    unique_factor = 5
    with open(filename) as f:
        data = json.load(f)
    logs = data["logs"]
    length = len(logs)
    index = len(logs)
    for i in range(index, length):
        if line_id == logs[i]["line_id"]:
            return False
    return True

def show_bot_output(comment, obj):
    print(comment)
    print(obj["text"])
    print(obj["ratio"])
    print()

def not_a_bot(author, bots):
    for bot in bots:
        if author == bot:
            return False
    return True   

def get_lines(filename):
    with open(filename) as f:
        data = json.load(f)
    lines = data["lines"]
    return lines

# Given all the bots responses, returns the one
# with the best match (highest ratio)
def get_best_ratio_res(*responses):
    bestResponse = responses[0]
    for response in responses:
        if response['ratio'] > bestResponse['ratio']:
            bestResponse = response
    return bestResponse

def get_best_response(text, *bots):
    best_res = bots[0].get_reply(text)
    for bot in bots:
        res = bot.get_reply(text)
        if res['ratio'] > best_res['ratio']:
            best_res = res
    return best_res

# Comment is valid if 
#   1. Longer than min_length
#   2. If one of our bots isn't the author.
#   3. The bots haven't replied to it.
def is_valid_comment(comment, bots):
    min_len = 20
    if len(comment.body) < min_len:
        return False
    for bot in bots:
        if comment.author == bot.get_username():
            return False
        accepted = bot.get_accepted_log()
        rejected = bot.get_rejected_log()
        for log in accepted:
            if log['comment_id'] == comment.id:
                return False
        for log in rejected:
            if log['comment_id'] == comment.id:
                return False
    return True

def run_the_bot(*bots):
    reddit = praw.Reddit('dwight-schrute-bot')
    accepted_ratio = 60
    for submission in reddit.subreddit('all').rising(limit=10):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if is_valid_comment(comment, bots):
                res = get_best_response(comment.body, dwight, michael)
                ratio = res['ratio']
                if ratio > accepted_ratio:
                    print(ratio)
                    print(res['name'])
                    print("COMMENT " + comment.body)
                    print("RESPONSE " + res['text'])
                    print()

def reply_comments(bot_name, lines_file, accepted_log, rejected_log):
    # If ratio meets set minimum, log comment & reply in accepted log.
    reddit = praw.Reddit(bot_name)
    lines = get_lines(lines_file)
    min_ratio = 50
    min_rej_ratio = 48
    for submission in reddit.subreddit("all").rising(limit=10):
        # Makes sure the last comment isn't a MoreComments object. 
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            bots = ["dwight-schrute-bot", "MichaelGScottBot", "andy-bernard-bot"]
            min_comment_len = 20
            if (not_a_bot(comment.author, bots) and len(comment.body) >= min_comment_len):
                obj = get_best_match(comment.body, lines)
                ratio = obj["ratio"]
                if ratio > 45:
                    print("COMMENT : " + comment.body + " RATIO : " + str(ratio))
                    print("REPLY " + obj["text"])
                    print()
                if ratio >= min_ratio:
                    log = accepted_log
                    if not is_logged(log, comment.id) and is_unique_comment(log, obj["id"]):
                        print("ACCEPTED")
                        comment.reply(obj["text"])
                        log_comment(log, obj, comment)
                        increm_reply_count(lines_file, obj["id"])
                        show_bot_output(comment.body, obj)
                        time.sleep(180)

                # If ratio meets rejected minimum, log comment & reply in rejected.
                elif ratio >= min_rej_ratio and not is_logged(rejected_log, comment.id):
                    print("REJECTED")
                    log_comment(rejected_log, obj, comment)
                    show_bot_output(comment.body, obj)

# Replies to comments & logs replies.
def run_bot(username, folder):
    print("RUNNING " + username)
    replies = folder + '/replies.json'
    accepted = folder + '/accepted_log.json'
    rejected = folder + '/rejected_log.json'
    reply_comments(username, replies, accepted, rejected)

def sleep_time(sleep_len):
    print("SLEEPING FOR " + str(sleep_len/60) + " MINUTES") 
    time.sleep(300)

if __name__ == "__main__":
    while (True):
        #run_bot('MichaelGScottBot', 'michael')
        #run_bot('dwight-schrute-bot', 'dwight')
        dwight = bot('dwight-schrute-bot', 'dwight')
        michael = bot('michaelGScottBot', 'michael')
        run_the_bot(dwight, michael)
        sleep_time(180)
        # run_bot('andy-bernard-bot', 'andy')
