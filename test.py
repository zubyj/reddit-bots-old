from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json

with open('dwight-replies.json') as f:
    data = json.load(f)

lines = data["lines"]

highestRatio = 0
theText = ""
comment = 'Say what you want about Michael Scott, but he never would\u2019ve done that.'
for line in lines:
    text = line["line"]["text"]
    ratio = fuzz.ratio(comment, text)
    if ratio > highestRatio:
        highestRatio = ratio
        theText = line["response"]["text"]

print(highestRatio)
print(theText)

