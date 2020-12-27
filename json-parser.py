import json

def write_json(data, filename="line-replies.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


with open('office-script.json') as f:
    data = json.load(f)

for line in data:
    if (line["speaker"] == "Dwight"):
        id = line["id"]
        # Gets index of character who spoke before dwight.
        id = int(line["id"])-2
        quote = data[id]["line_text"]
        response = (line["line_text"])
        print("Quote from " + data[id]["speaker"])
        #print(quote)
        print("Dwights response")
        #print(response)
        print()

        obj = {
            "quote":quote,
            "response":response
        }

        with open("line-replies.json") as json_file:
            data2 = json.load(json_file)
            temp = data2["lines"]
            temp.append(obj)

        write_json(data2)



        


















