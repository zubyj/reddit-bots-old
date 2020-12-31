
import json

with open('dwight-replies4.json') as f:
    data = json.load(f)

lines = data["lines"]

counter = 1
for line in lines:
    line["reply_count"] = 0
    line["accepted_ratio"] = 100
    line["id"] = counter
    counter+=1

with open('dwight-replies5.json', 'w') as f:
    json.dump(data, f, indent=4)