from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime

current_date = datetime.now().strftime('%Y%m%d')

# List of repos
REPOS = [
  'repo1',
  'repo2'
]

# Your Bitbucket cookies string (copy from browser)
BITBUCKET_COOKIES_STR = 'APP COOKIES'

def parse_cookies(cookie_str):
    cookies = []
    for cookie in cookie_str.split(';'):
        name, value = cookie.strip().split('=', 1)
        cookies.append({'name': name, 'value': value, 'domain': '.bitbucket.org'})
    return cookies

def add_cookies(driver, cookies):
    for cookie in cookies:
        driver.add_cookie(cookie)

# Parse the cookie string into a list of dictionaries
BITBUCKET_COOKIES = parse_cookies(BITBUCKET_COOKIES_STR)

def set_zoom_level(driver, zoom_level):
    driver.execute_script(f"document.body.style.zoom='{zoom_level}%'")

# Function to take screenshots of the given URLs
def take_screenshots(repos, zoom_level=65):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    # Navigate to Bitbucket to set cookies
    driver.get("https://bitbucket.org/")
    sleep(2)

    # Add cookies
    add_cookies(driver, BITBUCKET_COOKIES)

    for repo in REPOS:
        try:
            driver.get(f'https://bitbucket.org/WORKSPACE/{repo}/admin/branch-restrictions')
            sleep(2)

            set_zoom_level(driver, zoom_level)
            sleep(1)

            screenshot_filename = f"{repo}_{current_date}.png"
            driver.save_screenshot(screenshot_filename)
            print(f"Screenshot saved as {screenshot_filename}")

        except Exception as e:
            print(f"Error during processing {repo}: {e}")
    
    driver.quit()

take_screenshots(REPOS, zoom_level=65)
