import json


string_with_json = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},' \
                   '{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
obj = json.loads(string_with_json)
key = "messages"
if key in obj:
    second_message = obj[key][1]
    print(second_message["message"])
else:
    print(f"No key {key} in json")
