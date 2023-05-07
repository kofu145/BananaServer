import requests
"""payload = {"username": "kofu"}

r = requests.post('http://0.0.0.0:8080/signup', payload)

print(r.content)
print(r.json())
print(r.status_code)

r = requests.post('http://0.0.0.0:8080/login', payload)

print(r.content)
print(r.status_code)

auth_token = r.json()["auth"]
payload["auth"] = auth_token

post = {
	"author": "kofu",
	"content": "boo ya",
	"auth" : auth_token
	}

r = requests.post('http://0.0.0.0:8080/posts', post)

print(r.content)
print(r.json())
print(r.status_code)
payload = {"auth": auth_token}

r = requests.get('http://0.0.0.0:8080/posts', params=payload)

print(r.content)
print(r.json())
print(r.status_code)"""
files = {'image': open('can.jpg', 'rb')}
r = requests.post("https://127.0.0.1:8080/image", files=files)

with open("./test.jpg", 'wb') as f:
    f.write(r.content)