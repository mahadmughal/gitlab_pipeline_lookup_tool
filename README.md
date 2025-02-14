# GitLab Pipeline Lookup Tool

A Python script to search and filter GitLab pipelines by task name, environment, and status.

## Prerequisites

- Python 3.6 or higher
- Access to a GitLab instance
- GitLab personal access token with appropriate permissions

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>
cd gitlab-pipeline-lookup
```

2. Create a virtual environment:
```bash
# On Windows
python -m venv venv
.\venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

pip install -r requirements.txt

PROJECT_ID=your_project_id
GITLAB_ACCESS_TOKEN=your_gitlab_token

