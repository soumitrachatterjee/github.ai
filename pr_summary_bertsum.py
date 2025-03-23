import argparse
import json
import requests

def fetch_pr_details(pr_number, repo="llvm/llvm-project"):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching PR details: {response.status_code}")
        return None

def summarize_pr(pr_data):
    if not pr_data:
        return "Summary could not be generated due to insufficient discussion content."
    
    title = pr_data.get("title", "No Title")
    body = pr_data.get("body", "No Description")
    url = pr_data.get("html_url", "No URL")
    
    summary = f"**PR Summary:**\n{title}\n{body}\nFull PR: {url}"
    return summary

def main():
    parser = argparse.ArgumentParser(description="Fetch and summarize GitHub PRs.")
    parser.add_argument("--pr_number", type=int, help="Pull Request number", required=True)
    args = parser.parse_args()
    
    pr_data = fetch_pr_details(args.pr_number)
    summary = summarize_pr(pr_data)
    print(summary)

if __name__ == "__main__":
    main()
