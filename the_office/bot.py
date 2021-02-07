import praw
import json
from fuzzywuzzy import fuzz
from datetime import datetime
from datetime import time

class bot:
    def __init__(self, name, folder):

        # Logs into reddit account
        self.name = name
        self.account = praw.Reddit(name)

        # Get replies, accepted, rejected files. 
        self.folder = folder
        lines = folder + '/replies.json'
        self.accepted_path = folder + '/accepted_log.json'
        rejected = folder + '/rejected_log.json'
        with open(lines) as f, open(self.accepted_path) as f2, open(rejected) as f3:
            data1 = json.load(f)
            data2 = json.load(f2)
            data3 = json.load(f3)
        self.lines = data1['lines']
        self.accepted = data2['logs']
        self.rejected = data3['logs']
        self.reply = {}

    def get_username(self):
        return self.name

    def get_accepted_path(self):
        return accepted_path

    def get_folder(self):
        return self.folder

    def get_lines(self):
        return self.lines
    
    def get_accepted_log(self):
        return self.accepted
    
    def get_rejected_log(self):
        return self.rejected

    def get_account(self):
        return self.account
    
    def get_reply(self):
        return self.reply

    # Gets character's best response to given text. 
    def set_reply(self, text):
        highestRatio = 0
        bestLine = self.lines[0]
        for line in self.lines:
            reply = line['line']['text']
            ratio = fuzz.ratio(text, reply)
            if ratio > highestRatio:
                highestRatio = ratio
                bestLine = line
        self.reply =  {
            "name":self.name,
            "text":bestLine["response"]["text"],
            "ratio":highestRatio,
            "season":bestLine["season"],
            "episode":bestLine["episode"],
            "id":bestLine["id"],
        }

    def is_logged(self, comment_id):
        for log in self.get_accepted_log():
            if log['comment_id'] == comment_id:
                return True
        for log in self.get_rejected_log():
            if log['comment_id'] == comment_id:
                return True
        return False

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

    def del_bad_comments(self, comment):
        # Gets the deleted log
        filename = 'deleted.json'
        with open(filename) as f:
            data = json.load(f)
        temp = data["logs"]

        # Checks 5 past comments & deletes any under -3 karma.
        min_karma = -3
        my_account = self.account.redditor(self.name)
        for reply in my_account.comments.new(limit=5):
            if reply.score < min_karma:
                obj = {
                    "name":self.name,
                    "comment":comment,
                    "reply":reply.body,
                    "time":datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                }
                reply.delete()
                temp.append(obj)
        with open(filename, 'w') as f:
            json.dump(temp, f, indent=4)