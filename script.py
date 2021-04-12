from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import urllib, requests
import time
repeat = True
numBadRequest = 0
##todo:
## create class if can be open multiple firefox pointing to same url without having "bad gateaway" 
## for instance there is only one guichet, handle when they will open all others options
## send only notification when is succes
while repeat:
   # Creates a firefox handler
   firefoxOp = Options()
   firefoxOp.add_argument("--headless")
   browser = webdriver.Firefox(options=firefoxOp)
   # Opens url in handler
   browser.get("https://www.val-de-marne.gouv.fr/booking/create/4963")

   if numBadRequest > 10 :
      numBadRequest = 0
      print ("long wait cuz bad request")
      time.sleep(300)
   # try/exception when timeouts or bad gateaway
   try:
      # Set wait 10 seconds to find the labels below
      wait = WebDriverWait( browser, 10 )
      # label for the checkbox related to accept the conditions of RDV
      checkbox = browser.find_element_by_id("condition")
      # label for button to accept the RDV condition
      submit   = browser.find_element_by_name("nextButton")
      # Click on checkbox
      checkbox.click()
      # Click validate button
      browser.execute_script("arguments[0].click();",submit)
      # Set wait 15 seconds to find the labels below
      wait = WebDriverWait( browser, 15 )
      # Wait until the element appears
      wait.until(EC.element_to_be_clickable((By.ID, 'planning19604')))
      # Find labels
      checkbox = browser.find_element_by_id("planning19604")
      submit   = browser.find_element_by_name("nextButton")
      # Click labels
      checkbox.click()
      browser.execute_script("arguments[0].click();",submit)
      
      # 3rd page
      # Text when no RDV to assign
      textfromweb="Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."
      
      wait = WebDriverWait( browser, 15 )
      wait.until(EC.element_to_be_clickable((By.NAME, 'finishButton')))

       # Label which contains the message
      element = browser.find_element_by_id("FormBookingCreate")
      # If the same message found close and try again if not send a notification
      if textfromweb == element.text:
         print ("Jodido")
         browser.close()
         # Wait 20s before trying again
         time.sleep(20)
         # Url to send message with telegram bot: needs bot <token> chat <ID> and <message>
         url = "https://api.telegram.org/bot1777404851:AAFmqLmRJkeEmmO9uXzERhm6h_LaQz9r9-k/sendMessage?chat_id=-503195108&text=Fuckingjodido"
         requests.get(url)
      else:
         print ("telegram bot action")
         repeat = False

      # When ever everything is Ok this variable stay zero
 
   except:
      print("bad gateaway")
      print(numBadRequest)
      if numBadRequest > 9 :
         url = "https://api.telegram.org/bot1777404851:AAFmqLmRJkeEmmO9uXzERhm6h_LaQz9r9-k/sendMessage?chat_id=-503195108&text=killme"
         requests.get(url)
         print("Kill me")
         numBadRequest += 1
      else :
         numBadRequest += 1
      # Close the firefox handler
      browser.quit()


# In case of succes this send a messages to telegram with a succes message
url = "https://api.telegram.org/bot1777404851:AAFmqLmRJkeEmmO9uXzERhm6h_LaQz9r9-k/sendMessage?chat_id=-503195108&text=citacitacita"
print ("go to the site and launch again this script")
requests.get(url)
