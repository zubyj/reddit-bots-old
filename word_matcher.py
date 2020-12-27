from fuzzywuzzy import fuzz
import json

# Checks every line for closest match to phrase.
def get_best_match(phrase, lines):
    highestRatio = 0
    bestQuote = ""
    for line in lines:
        text = line["line"]
        ratio = fuzz.ratio(phrase, text)
        if ratio > highestRatio:
            highestRatio = ratio
            bestQuote = line["response"]["line"]
    obj = {
        "text":bestQuote,
        "ratio":highestRatio,
    }
    return obj
