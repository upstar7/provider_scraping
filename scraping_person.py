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

# Automatically manage ChromeDriver
driver_service = Service(ChromeDriverManager().install())

# Initialize WebDriver
driver = webdriver.Chrome(service=driver_service, options=chrome_options)

# Function to scrape a single page
def scrape_page(page_number):
    base_url = f"https://solicitors.lawsociety.org.uk/search/results?Pro=True&Type=1&Page={page_number}"
    driver.get(base_url)
    
    # Click the "Accept" button only on the first page
    if page_number == 1:
        try:
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "ccc-recommended-settings"))
            )
            accept_button.click()  # Click the "Accept" button
            print(f"Page {page_number}: Accept button clicked!")
        except Exception as e:
            print(f"Error on page {page_number}: {e}")
    
    # Scraping data
    data = []
    solicitors = driver.find_elements(By.CSS_SELECTOR, "section.solicitor-outer")

    for solicitor in solicitors:
        try:
            # Re-find each element within the loop to avoid stale references
            name_element = solicitor.find_element(By.CSS_SELECTOR, "header .heading h2 a")
            name = name_element.text.strip() if name_element else "N/A"

            try:
                employer_element = solicitor.find_element(By.CSS_SELECTOR, "dl dd.highlight a")
                employer = employer_element.text.strip() if employer_element else "N/A"
            except:
                employer = "N/A"

            # Handle multiple address lines
            address_elements = solicitor.find_elements(By.CSS_SELECTOR, "dl dd.feature.highlight")
            address = " ".join([addr.text for addr in address_elements]).strip() if address_elements else "N/A"

            try:
                phone_element = solicitor.find_element(By.CSS_SELECTOR, "dl dd.hidden-phone")
                phone = phone_element.text.strip() if phone_element else "N/A"
            except:
                phone = "N/A"

            # Append the data to the list
            data.append([name, employer, address, phone])
        except Exception as e:
            print(f"Error scraping solicitor data on page {page_number}: {e}")
            data.append(["N/A", "N/A", "N/A", "N/A"])  # In case of an error, add N/A for all fields

    return data

# Scraping multiple pages (1 to 30)
all_data = []
for page in range(1, 31):
    print(f"Scraping page {page}...")
    page_data = scrape_page(page)
    all_data.extend(page_data)
    time.sleep(2)  # Sleep to avoid overwhelming the server

# Close the browser once all pages are scraped
driver.quit()

# Create a DataFrame
df = pd.DataFrame(all_data, columns=["Name", "Employer", "Employer Address", "Phone"])

# Save to Excel
df.to_excel("solicitors_data_page_1_to_30.xlsx", index=False)

print("Data saved to 'solicitors_data_page_1_to_30.xlsx'")
