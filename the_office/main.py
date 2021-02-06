import praw
import json
from fuzzywuzzy import fuzz
from datetime import datetime
import time
from bot import bot

# Returns the bot with the best response to given text. 
def get_bot_best_reply(text, *bots):
    best_bot = bots[0]
    best_bot.set_reply(text)
    for bot in bots:
        bot.set_reply(text)
        ratio = bot.get_reply()['ratio']
        if ratio > best_bot.get_reply()['ratio']:
            best_bot = bot
    return best_bot

# Checks if reddit comment is valid. 
#   1. Longer than min_length
#   2. If one of the bots isn't the author.
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

# Writes reddit comment and bots response to given file.
def log_comment(self, comment):
    filename = self.get_folder() + '/accepted_log.json'
    data = self.get_reply()
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


def run_the_bots(*bots):
    reddit = bots[0].get_account()
    accepted_ratio = 70
    for submission in reddit.subreddit('all').rising(limit=15):
        submission.comments.replace_more(limit=None)
        if not submission.over_18:
            for comment in submission.comments.list():
                if is_valid_comment(comment, bots):
                    bot = get_bot_best_reply(comment.body, dwight, michael)
                    ratio = bot.get_reply()['ratio']
                    if not bot.is_logged(comment.id):
                        if ratio > accepted_ratio:
                                comment = bot.get_account().comment(id=comment.id)
                                bot_reply = bot.get_reply()['text']
                                comment.reply(bot_reply)
                                bot.log_comment(comment)
                                bot.del_bad_comments(bot_reply)
                                print(ratio)
                                print("COMMENT " + comment.body)
                                print(bot_reply)
                                print()
                                sleep_time(180)

def sleep_time(sleep_len):
    print("SLEEPING FOR " + str(sleep_len/60) + " MINUTES") 
    time.sleep(sleep_len)

if __name__ == "__main__":
    while (True):
        #run_bot('MichaelGScottBot', 'michael')
        #run_bot('dwight-schrute-bot', 'dwight')
        dwight = bot('dwight-schrute-bot', 'dwight')
        michael = bot('MichaelGScottBot', 'michael')
        print('RUNNING THE BOTS')
        run_the_bots(dwight, michael)
        # run_bot('andy-bernard-bot', 'andy')

# Makes sure every few comments are unique.
# def is_unique_comment(filename, line_id):
#     unique_factor = 5
#     with open(filename) as f:
#         data = json.load(f)
#     logs = data["logs"]
#     length = len(logs)
#     index = len(logs)
#     for i in range(index, length):
#         if line_id == logs[i]["line_id"]:
#             return False
#     return True
