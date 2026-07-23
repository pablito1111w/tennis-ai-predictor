import os
import csv
from datetime import datetime

import requests
from openai import OpenAI

from tennis_data import get_atp_matches


TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
OPENAI_KEY = os.environ["OPENAI_KEY"]


client = OpenAI(api_key=OPENAI_KEY)



# ---------------------------------------------
# AI ANALIZĖ
# ---------------------------------------------

def analyze(matches):

    matches_text = str(matches)

    prompt = f"""
Tu esi profesionalus ATP teniso analitikas.

Analizuok tik:

- ATP 500
- ATP Masters 1000
- Grand Slam


Duomenys:

{matches_text}


Atrink tik TOP 5 geriausius pasirinkimus.


Kiekvienam pateik:

🎾 Mačas:

🏆 Turnyras:

✅ Prognozė:

📊 Confidence procentas:

💰 Value pick:

📈 Tikėtinas rezultatas:

📝 Argumentai:


Vertink:

- dabartinę formą
- paskutinius 10 mačų
- dangą
- H2H
- servą
- return žaidimą
- fizinę būklę
- reitingų skirtumą
- galimą value


Jeigu nėra aiškaus pranašumo:
nerašyk pasirinkimo.


Formatas:

🎾 TOP ATP PICKS OF THE DAY

"""


    response = client.chat.completions.create(

        model="gpt-4.1-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )


    return response.choices[0].message.content




# ---------------------------------------------
# ISTORIJOS KAUPIMAS
# ---------------------------------------------

def save_history(prediction):

    file = "history.csv"

    exists = os.path.isfile(file)


    with open(
        file,
        "a",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)


        if not exists:
            writer.writerow(
                [
                    "date",
                    "prediction"
                ]
            )


        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d"),
                prediction.replace("\n", " ")
            ]
        )




# ---------------------------------------------
# TELEGRAM
# ---------------------------------------------

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




# ---------------------------------------------
# START
# ---------------------------------------------

matches = get_atp_matches()


# Jeigu nėra tinkamų ATP turnyrų

if matches["status"] == "empty":

    send_telegram(
        matches["message"]
    )

    print(
        "Nėra ATP TOP lygio mačų"
    )

    exit()



# Jeigu yra ATP mačai

prediction = analyze(
    matches["matches"]
)


save_history(prediction)


telegram_message = (
    "🎾 ATP DAILY PICKS\n\n"
    + prediction
)


send_telegram(
    telegram_message
)


print(
    "ATP prognozė išsiųsta"
)
