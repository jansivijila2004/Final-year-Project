from flask import Flask, request, render_template, redirect, url_for
from database import get_db
from security import detect_bruteforce, detect_injection
from datetime import datetime
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

BLOCK_FILE = "blocked_ips.txt"
LOG_FILE = "attack_log.txt"

# Email Configuration
EMAIL_USER = "projectmail0410@gmail.com"
EMAIL_PASSWORD = "jrlxdsdguzwxxbdm"
RECIPIENT_EMAIL = "jansivijila@gmail.com"


# ---------------- EMAIL ALERT ----------------
def send_email_alert(ip, attack_type):
    subject = f"Security Alert: {attack_type} Detected!"
    body = f"""
    SECURITY ALERT
    -----------------
    Attack Type: {attack_type}
    Attacker IP: {ip}
    Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("Email Error:", e)


# ---------------- IP BLOCK ----------------
def is_blocked(ip):
    try:
        with open(BLOCK_FILE, "r") as f:
            return ip in f.read().splitlines()
    except:
        return False


def block_ip(ip):
    if not is_blocked(ip):
        with open(BLOCK_FILE, "a") as f:
            f.write(ip + "\n")


# ---------------- LOG ----------------
def log_attack(ip, attack):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] IP: {ip} | Attack: {attack}\n")


# ---------------- HOME ----------------
@app.route("/home")
def home():
    logs = []
    total_blocked = 0

    try:
        with open(BLOCK_FILE, "r") as f:
            total_blocked = len(f.read().splitlines())
    except:
        pass

    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                match = re.search(r'\[(.*?)\] IP: (.*?) \| Attack: (.*)', line)
                if match:
                    logs.append({
                        "time": match.group(1),
                        "ip": match.group(2),
                        "type": match.group(3)
                    })
    except:
        pass

    logs.reverse()

    return render_template("home.html",
                           total_attacks=len(logs),
                           total_blocked=total_blocked,
                           recent_logs=logs[:10])


# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():

    ip = request.remote_addr

    if is_blocked(ip):
        return f"Your IP ({ip}) is blocked"

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # Injection Check
        if detect_injection(username) or detect_injection(password):
            block_ip(ip)
            log_attack(ip, "Injection")
            send_email_alert(ip, "Injection")
            return "Malicious Input Detected. IP Blocked"

        db = get_db()
        users = db["users"]

        user = users.find_one({
            "username": username,
            "password": password
        })

        if user:
            return redirect(url_for("home"))

        else:
            if detect_bruteforce(ip):
                block_ip(ip)
                log_attack(ip, "Brute Force")
                send_email_alert(ip, "Brute Force")
                return "Brute Force Detected. IP Blocked"

            return render_template("login.html", error="Invalid Login")

    return render_template("login.html")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)