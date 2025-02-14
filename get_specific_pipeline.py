import os
import gitlab
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class GitlabPipelineLookup:
    def __init__(self, status=None, ref=None):
        self.project_id = os.getenv('PROJECT_ID')
        self.gitlab_access_token = os.getenv('GITLAB_ACCESS_TOKEN')
        self.gitlab_url = f'https://devops.housing.sa:8083/api/v4/projects/{self.project_id}/pipelines'
        print("what project id: ", self.project_id)
        print("what access token: ", self.gitlab_access_token)
        self.headers = {
            'PRIVATE-TOKEN': self.gitlab_access_token
        }
        # Configure GitLab client
        self.gl = gitlab.Gitlab(
            url='https://devops.housing.sa:8083/',
            private_token=self.gitlab_access_token
        )
        self.gl.auth()
        self.project = self.gl.projects.get(self.project_id)
        try:
            filters = {
                'per_page': 100,
                'get_all': True
            }
            if status:
                filters['status'] = status
            if ref:
                filters['ref'] = ref

            self.pipelines = self.project.pipelines.list(**filters)
        except Exception as e:
            print(f"Error fetching pipelines: {e}")
            self.pipelines = None

    def get_pipeline_by_task_name(self, task_name):
        try:
            print(f"Connected to project: {self.project.name}")
            if not self.pipelines:
                print("Unable to fetch the pipelines")
                return None

            target_pipelines = []
            # Find pipeline by TASK_NAME
            for pipeline in self.pipelines:
                pipeline_name = pipeline.name
                if pipeline_name is not None and pipeline_name != '':
                    if task_name in pipeline_name:
                        target_pipelines.append(pipeline.attributes)

            if target_pipelines:
                print(f"Pipelines found: {target_pipelines}")
                return target_pipelines

            print(f"No pipeline found with task name: {task_name}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='GitLab Pipeline Lookup Tool')
    parser.add_argument('--task-name', required=True,
                        help='Task name to search for in pipeline names')
    parser.add_argument('--environment', choices=[
        'development', 'test', 'uat', 'production'],
        help='Task name to search for in pipeline names')
    parser.add_argument('--status', choices=[
        'created', 'pending', 'success', 'failed', 'canceled'],
        help='Filter pipelines by status')

    args = parser.parse_args()

    # Create GitlabPipelineLookup instance with optional status filter
    gitlab_lookup = GitlabPipelineLookup(
        status=args.status, ref=args.environment)
    pipeline = gitlab_lookup.get_pipeline_by_task_name(args.task_name)


if __name__ == "__main__":
    main()
