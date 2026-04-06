import smtplib
from email.mime.text import MIMEText

def send_alert(ip, attempts):
    sender_email = "projectmail0410@gmail.com"
    app_password = "jrlxdsdguzwxxbdm"   # ⚠️ Gmail App Password
    receiver_email = "jansivijila@gmail.com"

    subject = "🚨 Security Alert: Brute Force Attack Detected"

    body = f"""
Cyber Security Alert 🚨

Suspicious activity detected!

IP Address: {ip}
Failed Attempts: {attempts}

Status: IP has been BLOCKED automatically by the system.

Action Required: Check system logs immediately.
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("📧 Email sent successfully!")

    except Exception as e:
        print("❌ Email sending failed:", e)