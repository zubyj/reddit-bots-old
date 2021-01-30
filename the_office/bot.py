import json
from fuzzywuzzy import fuzz

class bot:
    def __init__(self, name):
        self.name = name
        lines_file = self.name + '/replies.json'
        with open(lines_file) as f:
            data = json.load(f)
        self.lines = data['lines']

    def get_lines(self):
        return self.lines

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
