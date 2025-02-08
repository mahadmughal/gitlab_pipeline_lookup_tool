from playwright.sync_api import sync_playwright, Browser  # type: ignore
from dotenv import load_dotenv
import time
import os


class GitLabPipelineManager:
    def __init__(self, environment: str = 'uat'):
        self.environment = environment
        load_dotenv()

    def execute_pipeline_flow(self):
        """Main method to execute the entire pipeline flow"""
        with sync_playwright() as playwright:
            self.browser_context = self._initialize_browser(playwright)
            self.page = self.browser_context.new_page()
            self._set_headers()

            try:
                self._run_pipeline_sequence()
            finally:
                self.browser_context.close()

    def _initialize_browser(self, playwright) -> Browser:
        """Initialize browser with required settings"""
        return playwright.chromium.launch_persistent_context(
            user_data_dir="./chrome-data",
            channel="chrome",
            headless=False,
            args=[
                '--enable-features=WebAuthenticationTouchId',
                '--password-store=basic',
                '--enable-biometric-authentication',
                '--enable-web-authentication-platform-apis',
                '--enable-features=InsecurePrivateNetworkRequestsAllowed',
                '--enable-features=WebAuthenticationPlatformAuthenticator',
                '--use-mock-keychain',
                '--allow-browser-signin',
                '--enable-web-auth-flow',
            ],
            permissions=['notifications', 'geolocation'],
            ignore_https_errors=True
        )

    def _set_headers(self):
        """Set required HTTP headers"""
        self.page.set_extra_http_headers({
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Sec-WebAuthn-UI": "true"
        })

    def _run_pipeline_sequence(self):
        """Execute the pipeline sequence in order"""
        self._login()
        print('User logged in successfully...')
        print("Now waiting for chrome-based system verification...")
        time.sleep(10)

        self._navigate_to_pipeline_page()
        self._select_environment()
        time.sleep(2)

        containers = self._get_ci_variable_containers()
        self._fill_pipeline_details(containers)
        self._execute_and_monitor_pipeline()

    def _login(self):
        """Handle login process"""
        self.page.goto('https://devops.housing.sa:8083/users/sign_in')
        self.page.wait_for_selector('#user_login')
        self.page.fill('#user_login', os.getenv('GITLAB_USERNAME'))
        self.page.fill('#user_password', os.getenv('GITLAB_PASSWORD'))
        self.page.locator('button[data-testid="sign-in-button"]').click()

    def _navigate_to_pipeline_page(self):
        """Navigate to the pipeline creation page"""
        self.page.goto(
            'https://devops.housing.sa:8083/ejar3/devs/ejar3-run-script-tool/-/pipelines/new')

    def _select_environment(self):
        """Select the specified environment"""
        self.page.locator('.ref-selector button.gl-button').first.click()
        self.page.locator(
            '[data-testid="base-dropdown-toggle"][aria-expanded="true"]'
        ).wait_for(state='visible')
        print('waiting for the options ...')

        dropdown_item = self.page.locator(
            f'[data-testid="listbox-item-refs/heads/{self.environment}"]')

        if dropdown_item.is_visible():
            print('Got the dropdown list items ...')
        dropdown_item.click()

    def _get_ci_variable_containers(self):
        """Get CI variable containers"""
        self.page.wait_for_selector(
            'div[data-testid="ci-variable-row-container"]')
        return self.page.locator(
            'div[data-testid="ci-variable-row-container"]')

    def _fill_pipeline_details(self, containers):
        """Fill all required pipeline details"""
        self._fill_ticket_number(containers.nth(0))
        print('Filled the ticket number ...')
        time.sleep(1)

        self._select_ejar3_service(containers.nth(1))
        print('selected Ejar service ...')
        time.sleep(1)

        self._insert_script(containers.nth(2))
        print('Inserted the script ...')
        time.sleep(3)

    def _fill_ticket_number(self, container):
        """Fill the NEOP ticket number"""
        div = container.locator('div')
        if div and (textarea := div.locator('textarea')):
            textarea.fill('NEOP ticket')

    def _select_ejar3_service(self, container):
        """Select the Ejar3 service from dropdown"""
        dropdown_div = container.locator(
            'div[data-testid="pipeline-form-ci-variable-value-dropdown"]')

        print("Select the Ejar3 service ...")
        print(dropdown_div)

        dropdown_btn = dropdown_div.locator(
            'button[data-testid="base-dropdown-toggle"]')
        dropdown_btn.click()

        dropdown_menu = self.page.locator('#base-dropdown-57')
        dropdown_menu.wait_for(state='visible')

        dropdown_items = self.page.locator('#base-dropdown-57 ul li')
        dropdown_items.nth(4).click()

    def _insert_script(self, container):
        """Insert Ruby script from file"""
        try:
            with open('script.rb', 'r') as file:
                ruby_script = file.read()

            if div := container.locator('div'):
                if textarea := div.locator('textarea'):
                    textarea.fill(ruby_script)
                    print('Successfully loaded and inserted script from script.rb')
        except FileNotFoundError:
            print("Error: script.rb file not found in the current directory")
        except Exception as e:
            print(f"Error reading script file: {str(e)}")

    def _execute_and_monitor_pipeline(self):
        """Execute pipeline and monitor its status"""
        self._run_pipeline()
        print('Executed the pipeline ...')
        time.sleep(1)

        self._navigate_to_pipeline_list()
        self._get_latest_pipeline()
        time.sleep(5)

    def _run_pipeline(self):
        """Run the pipeline"""
        run_pipeline_btn = self.page.locator(
            'button[data-testid="run-pipeline-button"]')
        run_pipeline_btn.click()

    def _navigate_to_pipeline_list(self):
        """Navigate to pipeline list page"""
        self.page.goto(
            'https://devops.housing.sa:8083/ejar3/devs/ejar3-run-script-tool/-/pipelines')
        self.page.wait_for_load_state('networkidle')
        print('Navigated to the pipelines list page ...')

    def _get_latest_pipeline(self):
        """Get the latest pipeline"""
        latest_pipeline = self.page.locator(
            '[data-testid="pipeline-table-row"]').nth(0)
        pipeline_link = latest_pipeline.locator(
            '[data-testid="pipeline-url-link"]')
        pipeline_link.click()

    def approve_pipeline(self):
        """Approve the pipeline (currently unused)"""
        approve_pipeline_btn = self.page.locator(
            '[data-testid="ci-action-button"]').nth(1)
        approve_pipeline_btn.click()


if __name__ == "__main__":
    pipeline_manager = GitLabPipelineManager()
    pipeline_manager.execute_pipeline_flow()
