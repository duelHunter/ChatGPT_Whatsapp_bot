from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time, requests
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException 


Chr_options = Options()
Chr_options.add_argument("user-data-dir=C:/Users/MSI/AppData/Local/Google/Chrome/User Data")
driver = webdriver.Chrome(options=Chr_options)
driver.get("https://web.whatsapp.com")

#wait for whatsapp web search bar
input_field = WebDriverWait(driver,60).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div[1]/p"))    
    )
input_field.send_keys("Chat GPT")
input_field.send_keys(Keys.ENTER)
time.sleep(4)

#local host url
url = "http://127.0.0.1:5000"

def get_current_time():
    now = datetime.now()
    formatted_time = now.strftime("[%I:%M %p, %d/%m/%Y]").lower()
    if formatted_time[1]=='0':
        formatted_time = '[' + formatted_time[2:]
    return formatted_time

def send_reply():
    return 0
def send_to_server(msg):
    response = requests.post(url, data=msg)
    time.sleep(3)
    print(response.content.decode('utf-8'))
    msg_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p")
    #send whatapp reply
    msg_box.send_keys(response.content.decode('utf-8'))
    msg_box.send_keys(Keys.ENTER)
    return 0


def check_for_msg():
    prev_msg = ""
    while True:
        try:
            received_messages = driver.find_elements(By.CLASS_NAME, "message-in")
            for message in received_messages:
                try:
                    msg_time_date = message.find_element(By.CSS_SELECTOR, '[data-pre-plain-text]').get_attribute('data-pre-plain-text')
                    msg_time_date_parts = msg_time_date.split(" ")

                    current_timedate_parts = get_current_time().split(" ")
                    
                    if msg_time_date_parts[0] == current_timedate_parts[0] and msg_time_date_parts[1] == current_timedate_parts[1] and msg_time_date_parts[2] == current_timedate_parts[2]:
                        msg_element = message.find_element(By.CSS_SELECTOR, '[dir]').get_attribute('dir')
                        if msg_element=='ltr':
                            msg_element = message.find_element(By.CSS_SELECTOR, '[dir]')
                            msg = msg_element.text

                            if msg != prev_msg:
                                send_to_server(msg)
                                print("Sent to server")
                                prev_msg = msg
                except StaleElementReferenceException:  # Added exception handling
                    print("Encountered a stale element reference, retrying...")
                    break  
        except Exception as e:
            print(e)
     
    

    

try:
    check_for_msg()
except Exception as e:
    print(e)
finally:
    driver.quit()



