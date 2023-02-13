import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

#Data[0] --> Date
#Data[1] --> Latitude
#Data[2] --> Longitude
#Data[3] --> Depth
#Data[4] --> Type
#Data[5] --> Size
#Data[6] --> Location
#Data[7] --> ID

bot_id="<bot_token>"
chat_id_log= "<chatid>"
chat_id_news="<log_channel_chatid>" # chat_id_news is optional. Is the log channel

def getData(): # Get data from url

    # Converting the data we access from the internet to python
    url = "https://deprem.afad.gov.tr/last-earthquakes.html"
    page = requests.get(url)    
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the datas
    data = []

    table = soup.find("table")
    rows = table.find_all("tr")

    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    return data[1]


def sendMessage(data): # Send message to Telegram

    # The content of the message to be sent
    text=f"· Yer: {data[6]}\n· Büyüklük: {data[5]}\n· Tarih: {data[0]}"
    try:
        # Telegram API connection
        send = requests.get(
            f'https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id_news}&text=' + str(
                text), timeout=2)

        if send.status_code > 299:
            print('TELEGRAM_ALARM_PUSH_ERROR: ', send.text)
        else:
            print('Message sent successfully.')

    except Exception as exc:
        print('telegram push error: ' + str(exc))

def sendReport(): # Send message to Telegram log channel. This function can be deleted if the log channel is not used
    text="working now time: " + str(datetime.datetime.now())
    try:
        # Telegram API connection
        send = requests.get(f'https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id_log}&text=' + text, timeout=2)

        if send.status_code > 299:
            print('TELEGRAM_ALARM_PUSH_ERROR: ', send.text)
        else:
            print('Message sent successfully.')

    except Exception as exc:
        print('telegram push error: ' + str(exc))


# It creates and saves the ID so that it does not send the last message again
lastMessage=0
# Sends notification when this number is a multiple of 6 (line:87)
reportNum=0

while True:
    data= getData()

    if not (lastMessage== data[-1]):
        if(float(data[5])>2.5):
            lastMessage=data[-1]
            sendMessage(data)

    if reportNum%60==0:
        sendReport()
        reportNum=0
        
    reportNum+=1
    time.sleep(5)