from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup




# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
dict = {}

def parseDocuments(document_url):
    url = document_url
    driver.get(url)

# Wait for the whole page to load by waiting for a specific element to appear
# You should replace 'someElementID' with an ID of an element known to appear late in the page load process
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'sect0045'))
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()

    # Get the HTML content
    html_content = driver.page_source

    # Close the browser
    driver.quit()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all elements that have an id containing 'sec'
    #section_elements = [element for element in soup.find_all(id=True) if 'sec' in element.get('id') or 'abs' in element.get('id')]

    for section in soup.find_all('section'):
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


    return dict











   
    

