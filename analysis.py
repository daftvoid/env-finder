import re

critical_patterns = [
    re.compile(r".*API_KEY$", re.IGNORECASE)
]

sensitive_patterns = [
    re.compile(r"SMTP_USER", re.IGNORECASE),
    re.compile(r"DB_HOST", re.IGNORECASE),
]

noise_patterns = [
    re.compile(r"^VITE.*", re.IGNORECASE)
]

def classify_env_key(key: str):
    key = key.strip().upper()

    for pattern in critical_patterns:
        if pattern.match(key):
            return "critical"
    for pattern in sensitive_patterns:
        if pattern.match(key):
            return "sensitive"
    for pattern in noise_patterns:
        if pattern.match(key):
            return "noise"

    return "unknown"

def analyze_env_file(content: str):
    result = []

    for line in content.split("\n"):
        if len(line.strip()) == 0: continue

        if line.startswith("#"): continue
        if "=" not in line: continue

        key, value = line.split("=", 1)

        key = key.strip().upper()
        value = value.strip()

        result.append({
            "severity": classify_env_key(key),
            "key": key,
            "value": value
        })

    return result

