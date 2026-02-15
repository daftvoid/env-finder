critical_env_vars = [
    "SMTP_PASS",
    "GEMINI_API_KEY"
]

sensitive_env_vars = [
    "SMTP_USER"
]

noise_env_vars = [
    "VITE_SUPABASE_PROJECT_ID",
    "NODE_ENV"
]

def analyze_env_file(content: str):
    result = []

    for line in content.split("\n"):
        if len(line.strip()) == 0: continue

        if line.startswith("#"): continue
        if "=" not in line: continue


        key, value = line.split("=", 1)

        key = key.strip().upper()
        value = value.strip()
        severity = "unknown"

        if key in critical_env_vars:
            severity = "critical"
        elif key in sensitive_env_vars:
            severity = "sensitive"
        elif key in noise_env_vars:
            severity = "noise"

        result.append({
            "severity": severity,
            "key": key,
            "value": value
        })

    return result

