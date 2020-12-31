import json

with open('dwight-replies5.json') as f:
    data = json.load(f)

lines = data["lines"]
id = input("Enter the line's ID to modify accepted ratio: ")
ratio = input("Enter the minimum ratio accepted to reply to the comment: ")

for line in lines:
    if (line["id"]) == int(id):
        line["accepted_ratio"] = ratio

with open('dwight-replies5.json', 'w') as f:
    json.dump(data, f, indent=4)