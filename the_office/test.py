import json
import praw
from main import get_best_match

reddit = praw.Reddit("MichaelGScottBot")
subreddit = reddit.subreddit("DunderMifflin")

with open("michael-replies2.json") as f:
    data = json.load(f)
lines = data["lines"]

# Open file of character's lines.
for comment in subreddit.stream.comments():
    obj = get_best_match(comment.body, lines)
    if obj["ratio"] > 50:
        print(comment.body)
        print(get_best_match(comment.body, lines))