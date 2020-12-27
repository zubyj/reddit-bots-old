from fuzzywuzzy import fuzz
import json

with open('line-replies2.json') as f:
    data = json.load(f)

lines = data["lines"]

phrase = "why don't you go to business"

highestRatio = 0
quote = ""
for line in lines:
    text = line["line"]
    ratio = fuzz.ratio(phrase, text)
    if ratio > highestRatio:
        highestRatio = ratio
        quote = line["response"]["line"]
print(quote)
print(highestRatio)
