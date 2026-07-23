import os
import csv
import requests


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]



def send_telegram(message):

    url = (
        "https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": message
        }
    )



def statistics():

    file = "history.csv"


    if not os.path.exists(file):

        return "Nėra istorijos duomenų"



    total = 0
    win = 0
    loss = 0


    with open(
        file,
        encoding="utf-8"
    ) as f:


        reader = csv.DictReader(f)


        for row in reader:

            total += 1


            if row["result"] == "WIN":
                win += 1


            if row["result"] == "LOSS":
                loss += 1



    accuracy = 0


    if total > 0:

        accuracy = round(
            win / total * 100,
            2
        )



    return f"""
🎾 ATP BOT STATISTIKA


Prognozių:
{total}


✅ WIN:
{win}


❌ LOSS:
{loss}


Tikslumas:
{accuracy}%

"""



message = statistics()

send_telegram(message)

print(message)
