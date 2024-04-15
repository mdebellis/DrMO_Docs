from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Enables headless mode
chrome_options.add_argument("--disable-gpu")  # Disables GPU hardware acceleration
chrome_options.add_argument("--window-size=1920x1080")  




# Set up WebDriver

dict = {}

def extract_content(section):
    # Find the first h2 or h3 tag as the title of the section
    title_tag = section.find(['h2', 'h3'])
    if title_tag:
        # Get the title text
        title_text = title_tag.get_text(strip=True)
        # Find all paragraph tags and concatenate their content
        paragraphs = section.find_all('p')
        content_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        # Add to your dictionary
        dict[title_text] = content_text

def parseDocuments(document_url,driver):
    url = document_url
    driver.get(url)

# Wait for the whole page to load by waiting for a specific element to appear
# You should replace 'someElementID' with an ID of an element known to appear late in the page load process
    
  
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, "//*[contains(@id, 'bib')]")
        )
    
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    # Get the HTML content
    html_content = driver.page_source

    # Close the browser


    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements that have an id containing 'sec'
    #section_elements = [element for element in soup.find_all(id=True) if 'sec' in element.get('id') or 'abs' in element.get('id')]

    for section in soup.find_all(lambda tag: tag.name == 'section' and 'cesectitle' in tag.get('id', '')):
        extract_content(section)
    
    for section in soup.find_all('section'):
        extract_content(section)



  


    return dict









   
    

