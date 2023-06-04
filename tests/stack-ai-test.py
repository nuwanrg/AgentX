import requests

API_URL = "https://www.stack-inference.com/run_deployed_flow?flow_id=645c40d9d91db619c024c16f&org=92ae61f8-572c-4f7c-b08e-a948fb3c8846"
headers = {'Authorization':
           'Bearer XXXXXXXXXXXXX',
           'Content-Type': 'application/json'
           }


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({"in-0": """What are the skills of Amal Gamage?"""})
print(output)
