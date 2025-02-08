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
    environment = 'test'

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


def run_pipeline(playwright):
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
        first_child = containers[0].query_selector('div')
        if first_child:
            textarea = first_child.query_selector('textarea')
            if textarea:
                textarea.fill('NEOP ticket')

        time.sleep(1)

        # Select Ejar service
        dropdown_div = containers[1].query_selector(
            'div[data-testid="pipeline-form-ci-variable-value-dropdown"]')
        if dropdown_div:
            dropdown_btn = dropdown_div.query_selector(
                '#dropdown-toggle-btn-55')
            dropdown_btn.click()

            dropdown_menu = page.locator('#base-dropdown-57')
            dropdown_menu.wait_for(state='visible')

            dropdown_items = page.locator('#base-dropdown-57 ul li')
            dropdown_items.nth(4).click()

        time.sleep(1)

        # Insert a script
        first_child = containers[2].query_selector('div')
        if first_child:
            textarea = first_child.query_selector('textarea')
            if textarea:
                textarea.fill("puts 'test pipeline'")

        time.sleep(1)

        # submit_button = page.locator(
        #     'button[data-testid="run-pipeline-button"]')
        # submit_button.click()

        # Wait for a moment
        time.sleep(10)

    finally:
        # Close the browser
        browser.close()


# Run the script
with sync_playwright() as playwright_gitlab:
    load_dotenv()
    run_pipeline(playwright_gitlab)
