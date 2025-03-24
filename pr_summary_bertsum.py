import requests
import configparser
import argparse

def load_config(config_file="config.ini"):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

def get_github_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code} - {response.text}")
        return None

def summarize_pr(pr_data):
    title = pr_data.get("title", "No Title")
    #body = pr_data.get("body", "No Description").split("\n")[0]  # First line as summary
    body = pr_data.get("body", "No Description")
    url = pr_data.get("html_url", "No URL")
    return f"**PR Summary:**\n{title}\n{body}\nFull PR: {url}"

def summarize_issue(issue_data):
    title = issue_data.get("title", "No Title")
    #body = issue_data.get("body", "No Description").split("\n")[0]  # First line as summary
    body = issue_data.get("body", "No Description")
    url = issue_data.get("html_url", "No URL")
    return f"**Issue Summary:**\n{title}\n{body}\nFull Issue: {url}"

def main():
    config = load_config()
    github_url = config["GitHub"]["api_url"]
    repo_owner = config["GitHub"]["repo_owner"]
    repo_name = config["GitHub"]["repo_name"]
    access_token = config["GitHub"]["access_token"]
    
    headers = {"Authorization": f"token {access_token}"}
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr_number", type=int, help="Pull request number")
    parser.add_argument("--issue_number", type=int, help="Issue number")
    args = parser.parse_args()
    
    if args.pr_number:
        pr_url = f"{github_url}/repos/{repo_owner}/{repo_name}/pulls/{args.pr_number}"
        pr_data = get_github_data(pr_url, headers)
        if pr_data:
            print(summarize_pr(pr_data))
    elif args.issue_number:
        issue_url = f"{github_url}/repos/{repo_owner}/{repo_name}/issues/{args.issue_number}"
        issue_data = get_github_data(issue_url, headers)
        if issue_data:
            print(summarize_issue(issue_data))
    else:
        print("Please provide either --pr_number or --issue_number")

if __name__ == "__main__":
    main()
