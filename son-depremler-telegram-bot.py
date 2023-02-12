import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


bot_id="bottoken_buraya_yazıacak"
chat_id_log= "log_kanalı_chatid_buraya_yazılacak"
chat_id_news="chatid_buraya_yazılacak" # İsteğe bağlı kullanılmayacaksa sendreport() fonksiyonu ve çağırıldığı yerler silinmeli.


def getData(): #son datayı getir

    url = "https://deprem.afad.gov.tr/last-earthquakes.html"
    page = requests.get(url)    
    soup = BeautifulSoup(page.content, "html.parser")

    # Verileri bul
    data = []

    table = soup.find("table")
    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    return data[1]

#Data[0] --> Tarih
#Data[1] --> Enlem
#Data[2] --> Boylam
#Data[3] --> Derinlik
#Data[4] --> Tip
#Data[5] --> Büyüklük
#Data[6] --> Konum
#Data[7] --> ID


def sendMessage(data):

    text=f"· Yer: {data[6]}\n· Büyüklük: {data[5]}\n· Tarih: {data[0]}"
    try:

        send = requests.get(
            f'https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id_news}&text=' + str(
                text), timeout=2)

        if send.status_code > 299:
            print('TELEGRAM_ALARM_PUSH_ERROR: ', send.text)
        else:
            print('Mesaj Başarıyla Gönderildi.')

    except Exception as exc:
        print('telegram push error: ' + str(exc))

def sendReport():
    text="working now time: " + str(datetime.datetime.now())
    try:
        send = requests.get(f'https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id_log}&text=' + text, timeout=2)

        if send.status_code > 299:
            print('TELEGRAM_ALARM_PUSH_ERROR: ', send.text)
        else:
            print('Mesaj Başarıyla Gönderildi.')

    except Exception as exc:
        print('telegram push error: ' + str(exc))



lastMessage=544856
reportNum=0

while True:
    data= getData()

    if not (lastMessage== data[-1]):
        if(float(data[5])>2.5):
            lastMessage=data[-1]
            sendMessage(data)

    if reportNum%60==0: # 5* bu sayı kadar saniye
        sendReport()
        reportNum=0
        
    reportNum+=1
    time.sleep(5)