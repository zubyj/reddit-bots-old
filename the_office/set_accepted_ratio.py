import json

filename = 'dwight-replies.json'

with open(filename) as f:
    data = json.load(f)

lines = data["lines"]
id = input("Enter the line's ID to modify: ")
ratio = input("Enter the minimum ratio accepted to trigger reply: ")

for line in lines:
    if (line["id"]) == int(id):
        line["accepted_ratio"] = ratio

with open (filename, 'w') as f:
    json.dump(data, f, indent=4)
