import requests

url = "https://api.todoist.com:443/rest/v2/tasks"

headers = {
    "Authorization": "Bearer 009c6c6e9d0b5bc61730aa5674fb6220c8025337"  # 替换为您的有效令牌
}
response = requests.get(url,headers=headers)
response = requests.get(url)
print(response.headers)
data = response.json()
print(data)