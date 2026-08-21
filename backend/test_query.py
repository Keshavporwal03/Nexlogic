import requests

params = {'q': 'Python location:"San Francisco"', 'per_page': 10}
r = requests.get('https://api.github.com/search/users', params=params)
print(r.url)
print(r.json().get('total_count'))
