# Removes personal directions from all lines and responses.
#
# Example 
#   Input : "Yes I will [Dwight starts doing karate]"
#   Output : "Yes I will"

import json

with open('dwight_replies2.json') as f:
    data = json.load(f)

lines = data["lines"]

counter = 0
for line in lines:
    theLine = line["line"]["text"]
    response = line["response"]["text"]

    while '[' in theLine:
        counter+=1  
        line1 = (theLine.split('[', 1)[0])
        line2 = (theLine.split(']', 1)[1])
        theLine = line1 + line2
        line["line"]["text"] = theLine
        print(theLine)

    while '[' in response:
        counter+=1  
        line1 = (response.split('[', 1)[0])
        line2 = (response.split(']', 1)[1])
        response = line1 + line2
        line["response"]["text"] = response
        print(response)

with open('dwight-replies3.json', 'w') as f:
    json.dump(data, f, indent=4)