from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# Specify the path to Chrome binary (default location on Kali Linux)
chrome_binary_path = '/usr/bin/google-chrome'

# Specify the path to ChromeDriver (using the user's home directory)
chrome_driver_path = '/home/bulwark/.cache/selenium/chromedriver/linux64/120.0.6099.109/chromedriver'

# Set up Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = chrome_binary_path

# Launch the web browser
driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)

# Open WhatsApp web
driver.get('https://web.whatsapp.com/')

# Wait for the user to scan the QR code and log in before proceeding

# Locate the chat input field
chat_input = driver.find_element("xpath", '//div[contains(@class, "copyable-text selectable-text")]')

# Set the contact number
contact_number = '03240606343'

# Send 100 messages
for i in range(100):
    time.sleep(1)  # Add delay to avoid rate limits
    chat_input.send_keys(f'Hello, message {i+1} to {contact_number}')
    chat_input.send_keys(Keys.ENTER)

# Close the web browser
driver.close()
