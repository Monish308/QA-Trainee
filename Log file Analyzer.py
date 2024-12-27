import re
from collections import Counter
from datetime import datetime

LOG_FILE_PATH = '/var/log/nginx/access.log' 

LOG_PATTERN = re.compile(r'(?P<ip>\S+) - - \[.*\] "(?P<method>\S+) (?P<url>\S+) \S+" (?P<status_code>\d+) \S+')

def analyze_log_file(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()

    status_codes = Counter()
    url_counts = Counter()
    ip_counts = Counter()

    for line in log_lines:
        match = LOG_PATTERN.match(line)
        if match:
            ip = match.group('ip')
            url = match.group('url')
            status_code = match.group('status_code')


            status_codes[status_code] += 1

            url_counts[url] += 1

            ip_counts[ip] += 1


    report = generate_report(status_codes, url_counts, ip_counts)

    return report
def generate_report(status_codes, url_counts, ip_counts):
    report = []

    report.append(f"Total 404 Errors: {status_codes.get('404', 0)}")

    most_requested_urls = url_counts.most_common(5)
    report.append("\nMost Requested Pages:")
    for url, count in most_requested_urls:
        report.append(f"  {url}: {count} requests")

    most_active_ips = ip_counts.most_common(5)
    report.append("\nTop 5 IPs with Most Requests:")
    for ip, count in most_active_ips:
        report.append(f"  {ip}: {count} requests")


    return "\n".join(report)

def main():
    print("Analyzing log file...")
    report = analyze_log_file(LOG_FILE_PATH)
    print("\nLog File Analysis Report:")
    print(report)

if __name__ == "__main__":
    main()
