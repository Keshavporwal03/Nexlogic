import requests

query = 'Java "Spring Boot" AWS location:"New York"'
url = f'https://api.github.com/search/users?q={query}&per_page=10'
print(url)
response = requests.get(url, headers={'Accept': 'application/vnd.github.v3+json'})
print('Status:', response.status_code)
data = response.json()
print('Total count:', data.get('total_count'))
