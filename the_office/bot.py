import json
from fuzzywuzzy import fuzz

class bot:
    def __init__(self, name, folder):
        self.name = name
        self.folder = folder
        lines = folder + '/replies.json'
        accepted = folder + '/accepted_log.json'
        rejected = folder + '/rejected_log.json'
        with open(lines) as f, open(accepted) as f2, open(rejected) as f3:
            data1 = json.load(f)
            data2 = json.load(f2)
            data3 = json.load(f3)
        self.lines = data1['lines']
        self.accepted = data2['logs']
        self.rejected = data3['logs']

    def get_username(self):
        return self.name

    def get_folder(self):
        return self.folder

    def get_lines(self):
        return self.lines
    
    def get_accepted_log(self):
        return self.accepted
    
    def get_rejected_log(self):
        return self.rejected

    # Gets character's best response to given text. 
    def get_best_response(self, text):
        highestRatio = 0
        bestLine = self.lines[0]
        for line in self.lines:
            reply = line['line']['text']
            ratio = fuzz.ratio(text, reply)
            if ratio > highestRatio:
                highestRatio = ratio
                bestLine = line
        return {
            "name":self.name,
            "text":bestLine["response"]["text"],
            "ratio":highestRatio,
            "season":bestLine["season"],
            "episode":bestLine["episode"],
            "id":bestLine["id"],
        }
