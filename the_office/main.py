import praw
import json
from fuzzywuzzy import fuzz
from datetime import datetime
import time
from bot import bot
from prawcore.exceptions import Forbidden


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
    #
    # Valid if 
    #   1. Our bots didnt write it.
    #   2. Our bots haven't yet replied to it.
    #   3. It's longer than min_length
    min_len = 15
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
    # Checks comments in past 15 rising posts.
    # Gets the best character response to given comment
    # If response ratio is higher than accepted ratio
    #   1. Reply to the comment with char response.
    #   2. Log the comment.
    #   3. Delete any past 5 replies with negative karma.
    #   4. Sleep for 3 minutes
    reddit = bots[0].get_account()
    accepted_ratio = 75
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
                            reply = bot.get_reply()
                            try:
                                comment.reply(reply['text'])
                            except Forbidden:
                                print(f"We\'ve been banned on r/{comment.subreddit}!")
                            bot.log_comment(comment)
                            bot.del_neg_comments()
                            sleep_time(120)

def sleep_time(sleep_len):
    print("SLEEPING FOR " + str(sleep_len/60) + " MINUTES") 
    print()
    time.sleep(sleep_len)

if __name__ == "__main__":
    while (True):
        dwight = bot('dwight-schrute-bot', 'dwight')
        michael = bot('MichaelGScottBot', 'michael')
        print('STARTING THE BOTS AGAIN')
        run_the_bots(dwight, michael)
        print('DONE RUNNING')
        sleep_time(180)
