from playwright.sync_api import sync_playwright, expect  # type: ignore
from dotenv import load_dotenv
import time
import os


def login(page):
    # Navigate to GitLab login page
    page.goto('https://devops.housing.sa:8083/users/sign_in')

    # Wait for and fill in the login form
    page.wait_for_selector('#user_login')
    page.fill('#user_login', os.getenv('GITLAB_USERNAME'))
    page.fill('#user_password', os.getenv('GITLAB_PASSWORD'))

    submit_button = page.locator('button[data-testid="sign-in-button"]')
    submit_button.click()


def select_environment(page):
    # Define valid environment
    environment = 'uat'

    # Click the dropdown using class selectors
    page.locator('.ref-selector button.gl-button').first.click()

    page.locator(
        '[data-testid="base-dropdown-toggle"][aria-expanded="true"]').wait_for(state='visible')

    print('waiting for the options ...')

    dropdown_item = page.locator(
        f'[data-testid="listbox-item-refs/heads/{environment}"]')

    if dropdown_item.is_visible():
        print('Got the dropdown list items ...')

    dropdown_item.click()


def fill_ticket_number(container):
    div = container.query_selector('div')
    if div:
        textarea = div.query_selector('textarea')
        if textarea:
            textarea.fill('NEOP ticket')


def select_ejar3_service(page, container):
    dropdown_div = container.query_selector(
        'div[data-testid="pipeline-form-ci-variable-value-dropdown"]')
    if dropdown_div:
        dropdown_btn = dropdown_div.query_selector(
            '#dropdown-toggle-btn-55')
        dropdown_btn.click()

        dropdown_menu = page.locator('#base-dropdown-57')
        dropdown_menu.wait_for(state='visible')

        dropdown_items = page.locator('#base-dropdown-57 ul li')
        dropdown_items.nth(4).click()


def insert_script(container):
    div = container.query_selector('div')
    if div:
        textarea = div.query_selector('textarea')
        if textarea:
            # pass a ruby script in string
            textarea.fill("puts 'test pipeline'")


def run_pipeline(page):
  run_pipeline_btn = page.locator(
      'button[data-testid="run-pipeline-button"]')
  run_pipeline_btn.click()


def approve_pipeline(page):
  approve_pipeline_btn = page.locator(
      '[data-testid="ci-action-button"]').nth(1)
  approve_pipeline_btn.click()


def get_latest_pipeline(page):
  latest_pipeline = page.locator(
      '[data-testid="pipeline-table-row"]').nth(0)
  pipeline_link = latest_pipeline.locator(
      '[data-testid="pipeline-url-link"]')
  pipeline_link.click()


def execute_gitlab_pipeline_flow(playwright):
    # Launch the browser
    browser = playwright.chromium.launch_persistent_context(
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
            '--use-mock-keychain',  # Enable system keychain access
            '--allow-browser-signin',
            '--enable-web-auth-flow',
            # '--enable-automation',

        ],
        # Only use valid permissions
        permissions=['notifications', 'geolocation'],
        ignore_https_errors=True
    )

    # Create a new page
    page = browser.new_page()
    page.set_extra_http_headers({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Sec-WebAuthn-UI": "true"  # Enable WebAuthn UI
    })

    try:
        login(page)

        print('User logged in successfully...')
        print("Now waiting for chrome-based system verification...")

        time.sleep(10)

        # Navigate to the pipeline page
        page.goto(
            'https://devops.housing.sa:8083/ejar3/devs/ejar3-run-script-tool/-/pipelines/new')

        select_environment(page)

        time.sleep(2)

        # Wait for and get CI variables' containers
        page.wait_for_selector('div[data-testid="ci-variable-row-container"]')
        containers = page.query_selector_all(
            'div[data-testid="ci-variable-row-container"]')

        # Fill NEOP-Ticket_Number
        fill_ticket_number(containers[0])

        print('Filled the ticket number ...')

        time.sleep(1)

        # Select Ejar service
        select_ejar3_service(page, containers[1])

        print('selected Ejar service ...')

        time.sleep(1)

        # Insert a script
        insert_script(containers[2])

        print('Inserted the script ...')

        time.sleep(3)

        run_pipeline(page)

        print('Executed the pipeline ...')

        time.sleep(1)

        # Navigate to the pipeline list page
        page.goto(
            'https://devops.housing.sa:8083/ejar3/devs/ejar3-run-script-tool/-/pipelines')

        page.wait_for_load_state('networkidle')

        print('Navigated to the pipelines list page ...')

        get_latest_pipeline(page)

        # approve_pipeline(page)

        # Wait for a moment
        time.sleep(5)

    finally:
        # Close the browser
        browser.close()


# Run the script
with sync_playwright() as playwright_gitlab:
    load_dotenv()
    execute_gitlab_pipeline_flow(playwright_gitlab)
