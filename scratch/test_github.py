import requests
import json
import urllib.parse
query = 'language:Python location:"New York, NY"'
url = f'https://api.github.com/search/users?q={urllib.parse.quote(query)}&per_page=10'
res = requests.get(url)
print("Language+Location status:", res.status_code)
print(json.dumps(res.json(), indent=2)[:500])

query2 = 'React Node location:"New York"'
url2 = f'https://api.github.com/search/users?q={urllib.parse.quote(query2)}&per_page=10'
res2 = requests.get(url2)
print("Skills status:", res2.status_code)
print(json.dumps(res2.json(), indent=2)[:500])
