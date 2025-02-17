# GitLab Pipeline Lookup Tool

A Python script to search and filter GitLab pipelines by task name, environment, status, date, and user who triggered the pipeline.

## Features

- Filter pipelines by task name
- Filter by environment (development, test, uat, production)
- Filter by pipeline status (created, pending, success, failed, canceled)
- Filter by date range (updated before/after specific dates)
- Filter by username who triggered the pipeline
- Combine multiple filters for precise searching

## Prerequisites

### Python Installation

1. Download Python:
   - Visit [Python's official website](https://www.python.org/downloads/)
   - Download the latest Python 3.x version (3.6 or higher)

2. Install Python:

   ```bash
   # Windows (During installation, make sure to check "Add Python to PATH")
   # Run in Command Prompt to verify installation
   python --version

   # macOS (Using Homebrew)
   brew install python3
   python3 --version

   # Linux - Ubuntu/Debian
   sudo apt update
   sudo apt install python3
   python3 --version

   # Linux - CentOS/RHEL
   sudo yum install python3
   python3 --version
   ```

### Pip Installation

1. Windows:

   ```bash
   # Python 3.x comes with pip by default. Verify installation:
   pip --version

   # If pip is not installed:
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python get-pip.py
   ```

2. macOS:

   ```bash
   # Using Homebrew (pip included if Python installed via Homebrew)
   brew install python3

   # Verify pip installation
   pip3 --version

   # If pip is not installed
   curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
   python3 get-pip.py
   ```

3. Linux:

   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3-pip
   pip3 --version

   # CentOS/RHEL
   sudo yum install python3-pip
   pip3 --version
   ```

### Other Requirements

- GitLab access token with appropriate permissions
- Project ID of the GitLab repository

## Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:mahadmughal/gitlab_pipeline_lookup_tool.git
   cd gitlab_pipeline_lookup_tool
   ```

2. Create a virtual environment:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a `.env` file in the root directory:

   ```bash
   touch .env
   ```

2. Add your GitLab credentials to the `.env` file:

   ```bash
   PROJECT_ID=your_project_id
   GITLAB_ACCESS_TOKEN=your_gitlab_token
   GITLAB_USERNAME=your_gitlab_username
   GITLAB_PASSWORD=your_gitlab_password
   GITLAB_BASE_URL=your_gitlab_base_url
   ```

## Usage

The script supports various filtering options that can be used individually or combined:

### Basic Search by Task Name

```bash
python3 get_specific_pipeline.py --task-name "NEOP-20473"
```

### Filter by Environment

```bash
python3 get_specific_pipeline.py --task-name "NEOP-20473" --environment production
```

### Filter by Status

```bash
python3 get_specific_pipeline.py --task-name "NEOP-20473" --status success
```

### Filter by Date Range

```bash
# Pipelines updated before a specific date
python3 get_specific_pipeline.py --task-name "NEOP-20473" --updated-before 2025-02-13

# Pipelines updated after a specific date
python3 get_specific_pipeline.py --task-name "NEOP-20473" --updated-after 2025-02-13
```

### Filter by Username

```bash
python3 get_specific_pipeline.py --task-name "NEOP-20473" --username 'm.asif'
```

### Combining Multiple Filters

```bash
python3 get_specific_pipeline.py --task-name "NEOP-20473" \
                                --environment uat \
                                --status failed \
                                --updated-before 2025-02-13 \
                                --updated-after 2025-02-13 \
                                --username 'm.asif'
```

## Available Filters

| Filter | Description | Available Options |
|--------|-------------|-------------------|
| `--task-name` | Search for specific task (Required) | Any string |
| `--environment` | Filter by environment | development, test, uat, production |
| `--status` | Filter by pipeline status | created, pending, success, failed, canceled |
| `--updated-before` | Show pipelines updated before date | YYYY-MM-DD format |
| `--updated-after` | Show pipelines updated after date | YYYY-MM-DD format |
| `--username` | Filter by user who triggered pipeline | GitLab username |

## Output

The script returns pipeline information including:

- Pipeline ID
- Status
- Creation date
- Last update date
- Triggered by (username)
- Environment
- Pipeline name
- Result status

## Error Handling

The script includes error handling for:

- Invalid date formats
- Connection issues
- Authentication failures
- Invalid project IDs
- API rate limiting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
