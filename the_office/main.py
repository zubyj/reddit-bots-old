import json
import praw
from fuzzywuzzy import fuzz
from datetime import datetime
import time
from bot import bot

def get_bot_best_reply(text, *bots):
    # Returns the bot with best reply to given text.
    best_bot = bots[0]
    best_bot.set_reply(text)
    for bot in bots:
        bot.set_reply(text)
        ratio = bot.get_reply()['ratio']
        if ratio > best_bot.get_reply()['ratio']:
            best_bot = bot
    return best_bot


def is_valid_comment(comment, bots):
    # Checks if reddit comment is valid
    # Valid if 
    #   1. Our bots didnt write the comment.
    #   2. Our bots haven't yet replied to the comment.
    #   3. The comment is long enough.
    min_len = 40
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

def run_the_bots(*bots):
    '''
    Here's the main algorithm

    1. Search  comments in the rising category
    2. If comment is close enough to a line in the show 
    2. Compare comment to every line our given character has responded to
    3. If the comment matches the line with a certainty, reply to the comment with our characters response.


    We do a few things when the match is detected
    1. Replies to the comment
    2. Logs the comment
    3. Deletes past replies with negative karma
    4. Search comments in the rising category
    5. Sleep for n minutes
    '''
    reddit = bots[0].get_account()
    accepted_ratio = 90
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
                                print(ratio)
                                print("COMMENT " + comment.body)
                                print(bot_reply)
                                print()
                                comment.reply(bot_reply)
                                bot.log_comment(comment)
                                # Deletes comments under -3 karma. 
                                # bot.del_bad_comments(bot_reply)
                                sleep_time(300)

def sleep_time(sleep_len):
    # Sleep for the specified time
    print("SLEEPING FOR " + str(sleep_len/60) + " MINUTES") 
    time.sleep(sleep_len)

if __name__ == "__main__":
    while (True):
        dwight = bot('dwight-schrute-bot', 'dwight')
        michael = bot('MichaelGScottBot', 'michael')
        print('RUNNING THE BOTS at ' + datetime.now().strftime("%H:%M:%S"))
        run_the_bots(dwight, michael)
        sleep_time(300)


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
