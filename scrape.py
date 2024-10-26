from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

AUTH = 'brd-customer-hl_037d6853-zone-ai_scapper:ghm6au5l97ct'
SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'

def scrape_website(website):
    print("Launching chrome browser...")

    # Connect using the updated ChromeDriver and Selenium settings
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    chrome_options = ChromeOptions()
    
    # Disable images, CSS, and JavaScript to speed up loading
    prefs = {
        "profile.managed_default_content_settings.images": 2,
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.stylesheets": 2,
        "profile.managed_default_content_settings.cookies": 2,
        "profile.managed_default_content_settings.javascript": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)

    # Run Chrome in headless mode for better performance
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # Maximize speed by disabling unnecessary features
    with Remote(sbr_connection, options=chrome_options) as driver:
        driver.get(website)
        
        # Adjust the wait time for CAPTCHA solving or loading
        print("Waiting briefly for CAPTCHA or content load...")
        time.sleep(5)  # Reduced wait time, adjust based on your observations
        
        print('Navigated! Scraping page content...')
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=60000):
    return [
        dom_content[i: i + max_length] for i in range(0, len(dom_content), max_length)
    ]
 




