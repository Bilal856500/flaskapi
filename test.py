import requests

BASE = 'http://127.0.0.1:5000/'


response = requests.put(BASE + "abc/1",  {"likes": 23})

print(response.json())
