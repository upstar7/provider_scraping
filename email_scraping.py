import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("--enable-unsafe-swiftshader")

driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

def get_email(profile_url):
    try:
        driver.get(profile_url)
        time.sleep(2)  # Allow the page to load

        # Locate the "Show" button
        try:
            show_button = driver.find_element(By.CSS_SELECTOR, "a#showhide.show_hide")
            # Scroll into view to ensure visibility
            driver.execute_script("arguments[0].scrollIntoView(true);", show_button)
            # Attempt to click the button
            driver.execute_script("arguments[0].click();", show_button)
            time.sleep(1)  # Allow the email to become visible
        except Exception as e:
            print(f"Show button not found or could not be clicked: {e}")

        # Now find the email
        try:
            email_element = driver.find_element(By.CSS_SELECTOR, "dd.slidingDiv a[href^='mailto:']")
            email = email_element.text.strip() if email_element else "N/A"
        except Exception as e:
            print(f"Email not found after clicking Show: {e}")
            email = "N/A"

        return email
    except Exception as e:
        print(f"Error retrieving email from {profile_url}: {e}")
        return "N/A"
profile_url = "https://solicitors.lawsociety.org.uk/person/1000220013/anil-motwani" 
email = get_email(profile_url)
print(email)
