import re

failed_attempts = {}

def detect_bruteforce(ip):
    if ip not in failed_attempts:
        failed_attempts[ip] = 0

    failed_attempts[ip] += 1

    if failed_attempts[ip] > 5:
        return True

    return False


# Optional basic injection check (for viva explanation)
def detect_injection(text):
    patterns = [r"\$", r"\{", r"\}", r"\bor\b", r"\band\b"]

    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False