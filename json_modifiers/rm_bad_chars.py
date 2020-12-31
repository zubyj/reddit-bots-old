# Removes personal directions from all lines and responses.
#
# Example 
#   Input : "Yes I will [Dwight starts doing karate]"
#   Output : "Yes I will"

import json

with open('dwight-replies3.json') as f:
    data = json.load(f)

lines = data["lines"]

counter = 0
for line in lines:
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
    print(line)
    print(response)

with open('dwight-replies4.json', 'w') as f:
    json.dump(data, f, indent=4)