import argparse
import configparser
import os
import requests
import json
from transformers import pipeline, BartTokenizer

# Load configuration
CONFIG_FILE = "config.ini"

def load_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config["GitHub"]

# Get GitHub Token from ENV
def get_github_token():
    token = os.getenv("GITHUB_PAT")
    if not token:
        raise ValueError("ERROR: GitHub PAT is missing. Set it using `export GITHUB_PAT=<your_token>`")
    return token

# GitHub API Helper Functions
def get_github_headers():
    token = get_github_token()
    return {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

def fetch_github_pr(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=get_github_headers())
    return response.json() if response.status_code == 200 else None

def fetch_github_issue(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=get_github_headers())
    return response.json() if response.status_code == 200 else None

# Summarization Function using BERTSUM
def summarize_text(text, max_length=150):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", tokenizer="facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    max_input_tokens = 1024  # BART's max token length
    input_tokens = tokenizer.encode(text, truncation=True, max_length=max_input_tokens)

    if len(input_tokens) > max_input_tokens:
        print(f"⚠️ Input text too long ({len(input_tokens)} tokens). Truncating to {max_input_tokens} tokens.")
        input_tokens = input_tokens[:max_input_tokens]
    
    # Convert tokens back to string for the model
    truncated_text = tokenizer.decode(input_tokens, skip_special_tokens=True)

    # Summarize with strict constraints
    summary = summarizer(truncated_text, max_length=max_length, min_length=50, truncation=True, do_sample=False)
    
    return summary[0]["summary_text"]

# Main Function to Process PRs or Issues
def process_github_request(pr_number=None, issue_number=None):
    config = load_config()
    owner, repo = config["repo_owner"], config["repo_name"]

    if pr_number:
        pr_data = fetch_github_pr(owner, repo, pr_number)
        if not pr_data:
            print(f"ERROR: PR #{pr_number} not found.")
            return
        
        title = pr_data["title"]
        body = pr_data.get("body", "No description provided.")
        summary = summarize_text(body)

        print(f"\nPR Summary:\nTitle: {title}\nSummary: {summary}\nFull PR: {pr_data['html_url']}")
    
    elif issue_number:
        issue_data = fetch_github_issue(owner, repo, issue_number)
        if not issue_data:
            print(f"ERROR: Issue #{issue_number} not found.")
            return
        
        title = issue_data["title"]
        body = issue_data.get("body", "No description provided.")
        summary = summarize_text(body)

        print(f"\nIssue Summary:\nTitle: {title}\nSummary: {summary}\nFull Issue: {issue_data['html_url']}")

# Argument Parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description="Summarize GitHub PRs and Issues.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pr_number", type=int, help="GitHub Pull Request number")
    group.add_argument("--issue_number", type=int, help="GitHub Issue number")
    return parser.parse_args()

# Run the script
if __name__ == "__main__":
    args = parse_arguments()
    process_github_request(pr_number=args.pr_number, issue_number=args.issue_number)

