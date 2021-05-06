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
## list of param: 
##   -webaddres
##   -enable background
##   -wait time?
##   -

checkbutonslist = ["planning19866","planning20424"]
listitem = 0
# update list with current month and delete all passed month
#lmonth = ["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Août","September","November","Décember"]
lmonth = ["Avril","Mai","Juin","Juillet","Août","September","November","Décember"]
rdvDict = {"Month":"","Id":""}
lRdv = []
listId = []
lValidId = []
firstRun = True
found = False
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
      time.sleep(150)
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
      wait = WebDriverWait( browser, 10 )
      # Wait until the element appears
      wait.until(EC.element_to_be_clickable((By.NAME, "planning")))

      if firstRun :
          # Gets all tags that have the name "planning", they have the all RDV
          checkbox = browser.find_elements_by_name("planning")
          for element in checkbox :
              # The attribute ID will point to the correct html tag 
              listId.append(element.get_attribute("id"))

          # Find all html tags  <labels> , this ones have the text which allows to know the naturalization type and the month
          labels = browser.find_elements_by_tag_name("label")
          # iterate all IDs
          for item in listId :
              # iterates all html tags found called labels 
              for element in labels :
                  # Match every label (it has the text that is needed) with the Id attribute
                  if found :
                     break
                  if element.get_attribute("for") == item :
                      # iterates the month available from current moment in the year
                      if found :
                          break
                      for month in lmonth :
                          # Is in the text is baturalization by decret and is in the following month from this current month
                          if "décret" in element.text and month in element.text :
                              # A dictionary with a valid id and valid month is created
                              rdvDict["Month"] = month
                              rdvDict["Id"] = item
                              # If there are many options a list is created
                              lRdv.append(rdvDict.copy())
                              found = True
                              break
              found = False            

          print("First Run")
          print(str(len(lRdv)))
          #print(lRdv)
          firstRun = False
      else :
          # Once the list of RDV is done, we iterate over it
          checkbox = browser.find_element_by_id(lRdv[listitem]["Id"])
          checkbox.click()
          submit   = browser.find_element_by_name("nextButton")
          # Click labels
          browser.execute_script("arguments[0].click();",submit)
    
          # 3rd page
          # Text when no RDV to assign
          textfromweb="Il n'existe plus de plage horaire libre pour votre demande de rendez-vous. Veuillez recommencer ultérieurement."
          
          wait = WebDriverWait( browser, 10 )
          wait.until(EC.element_to_be_clickable((By.NAME, 'finishButton')))

           # Label which contains the message
          element = browser.find_element_by_id("FormBookingCreate")
          # If the same message found close and try again if not send a notification
          if textfromweb == element.text:
             print ("Jodido")
             browser.close()
             # Wait 20s before trying again
             time.sleep(15)
             # Url to send message with telegram bot: needs bot <token> chat <ID> and <message>
             # The messages is updated with the month
             url = "https://api.telegram.org/bot1777404851:AAFmqLmRJkeEmmO9uXzERhm6h_LaQz9r9-k/sendMessage?chat_id=-503195108&text="+"No hay cita en: "+lRdv[listitem]["Month"]
             requests.get(url)
          else:
             print ("telegram bot action")
             repeat = False

          # To iterate in the list of Rdv that are not out of date 
          listitem += 1
          if listitem == len(lRdv):
              listitem = 0
      # clean list. not longer used
      listId = []
      lValidId = []
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
