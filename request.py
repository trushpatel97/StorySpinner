import requests

data=requests.get("https://regres.in/api/users")

print(data.text)