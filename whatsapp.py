
from selenium import webdriver
import time

# Set the path to the webdriver
driver = webdriver.Chrome('/mnt/data/chromedriver')

# Open Whatsapp Web
driver.get('https://web.whatsapp.com/')
time.sleep(15)

# Select the recipient
target = '"03439654513"'
x_arg = '//span[contains(@title,' + target + ')]'
group_title = driver.find_element_by_xpath(x_arg)
group_title.click()

# Send 100 messages
for i in range(100):
    input_box = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
    input_box.send_keys('Message ' + str(i))
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

# Close the webdriver
driver.close()
