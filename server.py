import socket
import smtplib
from email.mime.text import MIMEText

HOST = "0.0.0.0"
PORT = 5002

BLOCK_LIMIT = 6

failed_attempts = {}
blocked_ips = set()

# 📧 EMAIL ALERT FUNCTION
def send_alert(ip):
    sender = "projectmail0410@gmail.com"
    password = "jrlxdsdguzwxxbdm"
    receiver = "jansivijila@gmail.com"

    subject = "🚨 Security Alert: Brute Force Detected"
    body = f"""
Alert System Notification

IP Address: {ip}
Status: BLOCKED due to multiple failed login attempts.

Action: System automatically blocked this IP.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = receiver

    try:
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        print("📧 Email alert sent!")
    except Exception as e:
        print("❌ Email error:", e)


# 🖥️ SERVER SOCKET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print("🟢 Server Running...")
print("⏳ Waiting for connections...\n")

while True:
    client, addr = server.accept()
    ip = addr[0]

    print(f"\n🔗 Connected: {ip}")

    # 🚫 Blocked IP check
    if ip in blocked_ips:
        client.send("🚫 You are permanently blocked".encode())
        client.close()
        continue

    if ip not in failed_attempts:
        failed_attempts[ip] = 0

    while True:
        try:
            data = client.recv(1024).decode()

            if not data:
                print(f"❌ {ip} disconnected")
                break

            username, password = data.split(":")

            print(f"👤 {ip} -> {username} | {password}")

            # ✔ Correct login
            if username == "admin" and password == "Security@123":
                client.send("🟢 Login Success".encode())
                print("✅ Login successful")
                break

            # ❌ Wrong login
            failed_attempts[ip] += 1
            print(f"❌ Failed attempt {failed_attempts[ip]}/{BLOCK_LIMIT}")

            # 🚫 BLOCK CONDITION
            if failed_attempts[ip] >= BLOCK_LIMIT:
                blocked_ips.add(ip)
                print(f"🚨 IP BLOCKED: {ip}")

                send_alert(ip)

                try:
                    client.send("🚫 BLOCKED: Too many attempts".encode())
                except:
                    pass

                client.close()
                break

            else:
                client.send(f"🔴 Failed ({failed_attempts[ip]}/{BLOCK_LIMIT})".encode())

        except Exception as e:
            print("⚠️ Error:", e)
            client.close()
            break