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

# Any comment below the min karma gets deleted.
def del_bad_comments(bot):
    min_karma = -3
    account = bot.get_account()
    account = account.redditor(account.get_username())
    for comment in account.comments.new(limit=5):
        print(comment.body)
        print()
        if comment.score < min_karma:
            print('DELETED')
            print(comment.body)
            print(comment.score)
            print()
            comment.delete()

def run_the_bots(*bots):
    reddit = bots[0].get_account()
    accepted_ratio = 70
    for submission in reddit.subreddit('all').rising(limit=10):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if is_valid_comment(comment, bots):
                bot = get_bot_best_reply(comment.body, dwight, michael)
                ratio = bot.get_reply()['ratio']
                if not bot.is_logged(comment.id):
                    if ratio > accepted_ratio:
                            # the_comment is attached to bot that is going to reply. 
                            comment = bot.get_account().comment(id=comment.id)
                            comment.reply(bot.get_reply()['text'])
                            bot.log_comment(comment)
                            # bot.get_account().comment(id=comment.id).reply()
                            print(ratio)
                            print("COMMENT " + comment.body)
                            print(bot.get_reply()['text'])
                            print()
                            time.sleep(60)

def sleep_time(sleep_len):
    print("SLEEPING FOR " + str(sleep_len/60) + " MINUTES") 
    time.sleep(300)

if __name__ == "__main__":
    while (True):
        #run_bot('MichaelGScottBot', 'michael')
        #run_bot('dwight-schrute-bot', 'dwight')
        dwight = bot('dwight-schrute-bot', 'dwight')
        del_bad_comments(dwight)
        michael = bot('MichaelGScottBot', 'michael')
        run_the_bots(dwight, michael)
        # run_bot('andy-bernard-bot', 'andy')


# Function is called when bot replies to a comment.
# Increments the reply_count of line from given id.
# def increm_reply_count(filename, id):
#     with open(filename) as f:
#         data = json.load(f)
#     lines = data["lines"]
#     for line in lines:
#         if line["id"] == id:
#             count = line["reply_count"] +1
#             line["reply_count"] = count
#             print(count)
#             print(isinstance(count, str))
#             with open(filename, 'w') as f:
#                 json.dump(data, f, indent=4)
#                 return


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