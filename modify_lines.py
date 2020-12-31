import json

def add_attributes(lines):
    counter = 1
    for line in lines:
        line["reply_count"] = 0
        line["accepted_ratio"] = 100
        line["id"] = counter
        counter+=1

def rm_unknown_chars(line):
    theLine = line["line"]["text"]
    response = line["response"]["text"]

    while '\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd' in theLine:
        line1 = theLine.split('\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd', 1)[0]
        line2 = theLine.split('\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd', 1)[1]
        theLine = line1 + line2
        line["line"]["text"] = theLine

    while '\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd' in response:
        line1 = response.split('\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd', 1)[0]
        line2 = response.split('\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd', 1)[1]
        response = line1 + '\'' + line2
        line["response"]["text"] = response

def rm_line_dir(line):
    theLine = line["line"]["text"]
    response = line["response"]["text"]

    while '[' in theLine:
        line1 = (theLine.split('[', 1)[0])
        line2 = (theLine.split(']', 1)[1])
        theLine = line1 + line2
        line["line"]["text"] = theLine

    while '[' in response:
        line1 = (response.split('[', 1)[0])
        line2 = (response.split(']', 1)[1])
        response = line1 + line2
        line["response"]["text"] = response

def modify_lines(in_file, out_file):
    with open(in_file) as f:
        data = json.load(f)

    lines = data["lines"]
    for line in lines:
        rm_line_dir(line)
        rm_unknown_chars(line)
    
    with open(out_file, 'w') as f:
        json.dump(data, f, indent=4)

modify_lines('dwight-replies.json', 'dwight-replies2.json')