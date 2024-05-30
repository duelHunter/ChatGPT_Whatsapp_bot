from flask import Flask, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from undetected_chromedriver import Chrome

####################################################
options = Options()
# options.add_argument("user-data-dir=xsers/MSI/AppData/Local/Google/Chrome/User Data")
driver = Chrome(options=options)
driver.get("https://chat.openai.com")

prompt_area = WebDriverWait(driver,60).until(
   EC.presence_of_element_located((By.ID, 'prompt-textarea'))
)

####################################################
app = Flask(__name__)

@app.route('/', methods=['POST'])
def prompt_chatGPT():

   #get request from postman
   if request.method=='POST':
      data = request.data.decode('utf-8')
      try:
         prompt_area.send_keys(data)
         send_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/main/div[1]/div[2]/div[1]/div/form/div/div[2]/div/button')
         send_button.click()
      finally:
         gpt_answer = driver.find_elements(By.CLASS_NAME, 'markdown')

         return gpt_answer[-1].text

if __name__ == '__main__':
   app.run()
