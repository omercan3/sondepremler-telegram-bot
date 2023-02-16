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

now = datetime.datetime.now()

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

    # Converting the numeric date system to characteristic
    month = None
    monthstring = None
    date_str = data[0] # Access date data from datas
    date_dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") # Convert data to date format
    dateNumber = date_dt.month

    if dateNumber == 1:
        month = "Ocak" # January
    elif dateNumber == 2:
        month = "Şubat" # February
    elif dateNumber == 3:
        month = "Mart" # March
    elif dateNumber == 4:
        month = "Nisan" # April
    elif dateNumber == 5:
        month = "Mayıs" # May
    elif dateNumber == 6:
        month = "Haziran" # June
    elif dateNumber == 7:
        month = "Temmuz" # July
    elif dateNumber == 8:
        month = "Ağustos" # Agust
    elif dateNumber == 9:
        month = "Eylül" # September
    elif dateNumber == 10:
        month = "Ekim" # October
    elif dateNumber == 11:
        month = "Kasım" # November
    elif dateNumber == 12:
        month = "Aralık" # December

    monthstring = f'{date_dt.day} {month} {date_dt.year} / {date_dt.hour}:{date_dt.minute}'

    # The content of the message to be sent
    text=f"· Yer: {data[6]}\n· Büyüklük: {data[5]}\n· Tarih: {monthstring}"
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
    text=f"working now time: {now.hour}:{now.minute}+ -1001733553587"
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
lastMessage = 0
# Log channel counter
reportNum = 0
# Shares earthquakes above this magnitude
magnitude = 2.5

while True: # Delete sendReport() and reportNum if you are not going to use the log system
    data= getData()

    if not (lastMessage== data[-1]):
        if(float(data[5])>magnitude):
            lastMessage=data[-1]
            sendMessage(data)

    # reportNum / 5 = time to throw log message
    if(reportNum == 90):
        sendReport()
        reportNum = 0

    reportNum += 1
    time.sleep(5)