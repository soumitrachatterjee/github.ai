# github.ai
Intelligent analytics on GitHub essentials

## GitHub Summarizer
This project provides a tool to fetch and summarize GitHub Pull Requests and Issues using the GitHub API. The script supports configurable settings through an INI file, making it flexible and easy to use.

### Features
Fetches details of a GitHub Pull Request (PR) and provides a summary.
Fetches details of a GitHub Issue and provides a summary.

Configurable via `config.ini` for GitHub repository details and authentication.

### Prerequisites

Ensure you have Python 3 installed on your system. You can check this by running:
```
python3 --version
```

#### Installation

Clone this repository:
```
git clone https://github.com/your-repo/github-summarizer.git
cd github-summarizer
```

#### Install dependencies:
```
pip install -r requirements.txt
```

### Configuration

Before running the script, configure your GitHub API settings by creating a config.ini file in the project directory. Example:
```
[github]
api_url = https://api.github.com
repo_owner = llvm
repo_name = llvm-project
token = your_personal_access_token
```

Replace your_personal_access_token with a valid GitHub personal access token (PAT) to authenticate API requests.

If you don’t have a GitHub PAT, generate one from GitHub Developer Settings.

### Usage

#### Summarizing a Pull Request

To fetch and summarize a GitHub Pull Request:
```
python3 summarize.py --pr_number 132529
```

#### Summarizing an Issue

To fetch and summarize a GitHub Issue:
```
python3 summarize.py --issue_number 12345
```

#### Example Output
```
**PR Summary:**
[RISCV] Remove experimental from Sdext and Sdtrig which are ratified.
They were ratified in February 2025.
Full PR: https://github.com/llvm/llvm-project/pull/132529
```

### Troubleshooting

*Invalid Token Error:* Ensure your GitHub token has the necessary repository access.

*Rate Limit Exceeded:* GitHub API imposes rate limits; try again later or use a token with higher limits.

*Missing Configurations:* Double-check config.ini for missing or incorrect values.

