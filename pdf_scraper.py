from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
from selenium.common.exceptions import JavascriptException


# Configure Selenium WebDriver
driver = webdriver.Chrome()

#http://dx.doi.org/10.1002/14651858.CD005620.pub3


driver.get('https://www.cochranelibrary.com/cdsr/doi/10.1002/14651858.CD005620.pub3/epdf/abstract')


#download_pdf_dropdown = WebDriverWait(driver, 10).until(
    #EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pulldown-menu-trigger"))
#)
#download_pdf_dropdown.click()

# Wait for the dropdown menu items to appear
"""
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "ul.pulldown-menu-items"))
)
"""

# Locate the second item in the dropdown and click it
"""
second_dropdown_item = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "ul.pulldown-menu-items > li:nth-child(2) > a"))
)
"""



    # Click the 'next page' button


driver.implicitly_wait(10)

# Use JavaScript to click on the element
# This JavaScript snippet will attempt to click the element directly,
# bypassing the usual DOM methods if the element is nested within shadow DOMs
try:
    driver.execute_script("""
        var element = document.querySelector('menu-button.download');
        if (element) {
            element.click();
        } else {
            throw new Error('Element not found');
        }
    """)
except JavascriptException as e:
    print(f"JavaScript error occurred: {e}")
# Now wait for the "Download PDF" option within the dropdown to be clickable


# Wait for the "Download PDF" button to be clickable



# After clicking, check for the result of the click.
# For example, if a dialog opens or a new element appears, wait for that element to confirm the click worked.
