from collections import Counter

def escalate_errors(logs, threshold=3):
    """Mark errors as critical if they repeat more than threshold times"""
    error_counts = Counter([log["Error"] for log in logs])
    for log in logs:
        if error_counts[log["Error"]] >= threshold:
            log["Severity"] = "Critical"
        else:
            log["Severity"] = "Normal"
    return logs