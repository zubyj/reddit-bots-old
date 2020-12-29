import json

with open('dwight_replies2.json') as f:
    data = json.load(f)

lines = data["lines"]

counter = 0
for line in lines:
    theLine = line["line"]["text"]
    response = line["response"]["text"]


    min = 30
    if '[' in theLine and len(theLine) < min:
        counter+=1
        print(theLine)
        print()

print(counter)