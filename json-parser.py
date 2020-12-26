import json

with open('office-script.json') as f:
    data = json.load(f)

for line in data:
    if (line["speaker"] == "Dwight"):
        id = line["id"]
        # Gets id of character before dwights line.
        id = int(id)-2
        quote = data[id]["line_text"]
        response = (line["line_text"])
        print("Quote from " + data[id]["speaker"])
        print(quote)
        print("Dwights response")
        print(response)




