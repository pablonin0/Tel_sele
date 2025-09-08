from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time as ti

from bs4 import BeautifulSoup
from dateutil.parser import parse
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# ---------- SQLAlchemy ORM Setup ----------

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    contentClean = Column(String)
    contentRaw = Column(Text)
    GroupName = Column(String)
    timestamp = Column(DateTime, default=datetime.now)

# Create SQLite DB and session
engine = create_engine("sqlite:///DB&Imgs/messages.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ---------- Selenium Setup ----------

def OpenChat (chatNameLink):
        #open second tab and switch
    link2 = f'https://web.telegram.org/k/#@{chatNameLink}'

    driver.execute_script("window.open('');")
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])
    #open second link
    driver.get(link2)
    #driver.refresh
    print('GRUOP OPENED')
    ti.sleep(15)
    driver.save_screenshot('DB&Imgs/tempImg/1-GRUP.png') 


print('1.Start')

#Options to run headless
options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")  
options.add_argument("--no-sandbox")  
options.add_argument("--disable-dev-shm-usage")  

# Optional: reduce console logs
options.add_argument("--log-level=3")
# Start browser
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

#driver = webdriver.Chrome(ChromeDriverManager().install())

print('2.Selenium Running')
print('3.Login')

#open first link
link1 = 'https://web.telegram.org/'
driver.get(link1)
ti.sleep(8)

inputSuccess = 'n'

while(inputSuccess != 'y'):
    driver.save_screenshot('DB&Imgs/tempImg/QR.png')
    print('Waiting Login print | y | if logged and | n | if not')
    inputSuccess = input()

print('LOGIN SUCCESFULLLLL!!!!')


print('4.Open group')

print('4.1 Ingrese el grupo')

GruopNameLink = input()

if GruopNameLink == '':
    GruopNameLink = 'OFERTAESPECIALESMXX'

OpenChat(GruopNameLink)


#https://web.telegram.org/k/#@OfertasydealsBot
#open second tab and switch
link2 = f'https://web.telegram.org/a/#?tgaddr=tg%3A%2F%2Fresolve%3Fdomain%{GruopNameLink}'




#stores messages text as a list
messages_text = []

# Define the full class list you're looking for
class_list = [
        "Message", "message-list-item", "first-in-group",
        "allow-selection", "last-in-group", "has-views",
        "shown", "open"
    ]

    
#text-content clearfix with-meta
class_list_text = [
    'text-content', 'clearfix', 'with-meta'
    ]
countPulls = 0


#cleans the db of previous messages
session.query(Message).delete()

print('5.pulling info')

while True:
    
    #gets the body element
    #var = driver.find_element(By.TAG_NAME, 'body')
    #from te body element extract all the body info un like page source that is limited
    #var5 = driver.execute_script("return document.body.innerHTML")
    #html_content = var.get_attribute('innerHTML')
   
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')
    
    


     
    #gettin al te children of messages container
    # Build the CSS selector
    # Get the container element       
    selectorAll = '.messages-container'
    date_group = soup.select_one(selectorAll)
    MsgContFalse = False
    if date_group is not None:
        Messages_divs = date_group.select('.text-content.clearfix.with-meta')
        MsgContFalse = True
    
    BBulFalse = False
    if date_group is None:
        all_bubbles = soup.select(".bubbles-inner")
        date_group = all_bubbles[1]

        Messages_divs = date_group.select('.translatable-message')
        BBulFalse = True
        
   

   


    

    
    #in message_elements
    count = 0
    if countPulls == 0:
        RepetedMsgTest = []
    

    for message in Messages_divs:
        
        textAll = message.get_text(separator="/n", strip=True)
        text = message.get_text(separator="  #  ", strip=True)

        #if countPulls == 0:
        #    RepetedMsgTest.append('a')
    

        #if RepetedMsgTest[count] == text :
        #   break  

       
        #print
        print('--------------------------------------')
        print(text)
        messages_text.append(text)
        #db
        msgDb = Message(contentClean = textAll, contentRaw = text, GroupName = GruopNameLink)
        session.add(msgDb)
        count +=1
    count = 0
    session.commit()  
    
    RepetedMsgTest = messages_text
    RepetedMsgTestTwo = messages_text
    print('-----------------------')
    print(len(messages_text))

    if len(messages_text) >= 700:
        session.query(Message).delete()
        messages_text.clear()


    #driver.execute_script("""
    #document.querySelector('.MessageList').scrollTop -= 400;
    #""")

    #si en el messae froup no hay 21 divs 

    countPulls +=1

    #scoll to the bottom using js
    if MsgContFalse is True:
        driver.execute_script("""
            document.querySelector('.MessageList').scrollTop = 
            document.querySelector('.MessageList').scrollHeight;
            """)
    

    if BBulFalse is True:
        driver.execute_script("""
            document.querySelector('.bubbles>.scrollable').scrollTop = 
            document.querySelector('.bubbles>.scrollable').scrollHeight;
            """)
    
    
    #añadir el randomness
    ti.sleep(1)


   



ti.sleep(1000)  # Give yourself time to scan QR code or log in

driver.quit()

