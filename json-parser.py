import json

def write_json(data, filename="line-replies2.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def is_legit(line):
    return isinstance(line, str) and len(line) > 20

with open('office-script.json') as f:
    data = json.load(f)

with open('line-replies2.json') as f2:
    data2 = json.load(f2)

for line in data:
    text = line["line_text"]
    speaker = line["speaker"]
    if speaker == "Dwight" and is_legit(text):
        # Gets the line before dwight's.
        prevIndex = int(line["id"])-2
        prevLine = data[prevIndex]
        prevSpeaker = prevLine["speaker"]
        prevText = prevLine["line_text"]
        if prevSpeaker != "Dwight" and is_legit(prevText):
            obj = {
                "character":prevSpeaker,
                "line":prevText,
                "response" : {
                    "character":speaker,
                    "line":text
                }
            }
            temp = data2["lines"]
            temp.append(obj)
            write_json(data2)


        


















