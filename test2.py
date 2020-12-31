import json


# Checks comments by the unique_factor value.
# Ex. if unique_factor is 5, past 5 comments must be unique.
def is_unique_comment(filename, line_id):
    unique_factor = 5

    with open(filename) as f:
        data = json.load(f)
    logs = data["logs"]
    length = len(logs)
    index = length-5
    for i in range(index, length):
        if line_id == logs[i]["line_id"]:
            return False
    return True

print(is_unique_comment('comment_log.json', 1305))