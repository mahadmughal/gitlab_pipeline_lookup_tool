# GitLab Pipeline Lookup Tool

A Python script to search and filter GitLab pipelines by task name, environment, and status.

## Prerequisites

- Python 3.6 or higher

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

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
```bash
PROJECT_ID=your_project_id
GITLAB_ACCESS_TOKEN=your_gitlab_token
GITLAB_USERNAME=your_gitlab_username
GITLAB_PASSWORD=your_gitlab_password
GITLAB_ACCESS_TOKEN=your_gitlab_access_token
PROJECT_ID=your_gitlab_project_id
```
