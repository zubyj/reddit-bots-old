
import json

def is_valid_line(line):
    min_length = 20
    return isinstance(line, str) and len(line) > min_length

# char_name should be the desired TV character's first name.
def get_line_obj(line, char_name):
    speaker = line["speaker"]
    text = line["line_text"]
    if is_valid_line(text) and speaker == char_name:
        prevIndex = int(line["id"]-2)

# Gets the line object
def get_line_obj(line):
     return {
        "character":line["speaker"],
        "text":line["line_text"]
    }

# Gets every response from given "The Office character"
# Also, gets every line and character and triggered the response. 
# The lines & responses stored in given json file. 
def get_lines(char_name, out_file):
    with open('office-script.json') as f:
        data = json.load(f)
    with open(out_file) as f:
        out_data = json.load(f)
    for line in data:
        text = line["line_text"]
        speaker = line["speaker"]
        if is_valid_line(text) and speaker == char_name:
            # Gets index of the previous line
            prevIndex = int(line["id"]) - 2
            prevLine = data[prevIndex]
            prevText = prevLine["line_text"]
            # If prev line is valid and isn't from same speaker
            if is_valid_line(prevText) and prevLine["speaker"] != char_name:
                theLine = get_line_obj(prevLine)
                theResponse = get_line_obj(line)
                obj = {
                    "season":line["season"],
                    "episode":line["episode"],
                    "line":theLine,
                    "response":theResponse
                }

                temp = out_data["lines"]
                temp.append(obj)
                with open(out_file, 'w') as f:
                    json.dump(out_data, f, indent=4)

# Gets all lines from the character, "Dwight Schrute"
get_lines('Dwight', 'dwight_replies.json')

# Gets all lines from the character, "Michael Scott"
# get_lines('Michael', 'michael_replies.json')