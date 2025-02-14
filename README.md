# GitLab Pipeline Lookup Tool

A Python script to search and filter GitLab pipelines by task name, environment, and status.

## Prerequisites

- Python 3.6 or higher

1. Clone the repository:
```bash
git clone git@github.com:mahadmughal/gitlab_pipeline_automation_tool.git
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
```

5. Run the script:
```bash
# Search for a specific task:
python3 get_specific_pipeline.py --task-name "NEOP-20473"

# Search for a task in a specific environment:
python3 get_specific_pipeline.py --task-name "NEOP-20473" --environment production

# Search for a task with specific status:
python3 get_specific_pipeline.py --task-name "NEOP-20473" --status success

# Combine multiple filters:
python3 get_specific_pipeline.py --task-name "NEOP-20473" --environment uat --status failed
```
