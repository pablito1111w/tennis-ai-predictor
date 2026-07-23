import os
import csv
from datetime import datetime

import requests
from openai import OpenAI

from tennis_data import get_atp_matches



TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
OPENAI_KEY = os.environ["OPENAI_KEY"]



client = OpenAI(
    api_key=OPENAI_KEY
)



# --------------------------------------------------
# AI ANALIZĖ
# --------------------------------------------------

def analyze(matches):


    matches_text = str(matches)



    prompt = f"""

Tu esi profesionalus ATP teniso analitikas ir value betting specialistas.


Analizuok tik:

- ATP 500
- ATP Masters 1000
- Grand Slam


Duomenys:

{matches_text}



Atrink tik geriausius ATP pasirinkimus.


Maksimaliai:
5 pick'ai per dieną.



Kiekvienam pateik:


🎾 Mačas:

🏆 Turnyras:

✅ Prognozė:

📊 Tikimybė procentais:

💰 Koeficientas:

📈 Value procentas:

🎯 Statusas:

VALUE PICK arba SKIP



Vertink:


- ATP reitingą
- paskutinių 10 mačų formą
- dangą
- H2H
- servą
- return žaidimą
- fizinę būklę
- koeficiento vertę



TAISYKLĖ:


Jeigu nėra aiškaus pranašumo:

NERODYK pasirinkimo.



Jeigu nėra koeficientų:

rašyk:

NO ODDS DATA



Jeigu value mažiau nei 5%:

SKIP.



Formatas:


🎾 TOP ATP VALUE PICKS OF THE DAY

"""



    response = client.chat.completions.create(


        model="gpt-4.1-mini",


        messages=[

            {

                "role":
                "user",

                "content":
                prompt

            }

        ]

    )


    return response.choices[0].message.content





# --------------------------------------------------
# ISTORIJA
# --------------------------------------------------

def save_history(prediction):


    file = "history.csv"


    exists = os.path.isfile(
        file
    )



    with open(

        file,

        "a",

        newline="",

        encoding="utf-8"

    ) as f:



        writer = csv.writer(
            f
        )



        if not exists:

            writer.writerow(

                [

                    "date",

                    "prediction",

                    "result",

                    "profit"

                ]

            )



        writer.writerow(

            [

                datetime.now().strftime(
                    "%Y-%m-%d"
                ),

                prediction.replace(
                    "\n",
                    " "
                ),

                "PENDING",

                ""

            ]

        )





# --------------------------------------------------
# TELEGRAM
# --------------------------------------------------

def send_telegram(message):


    url = (

        "https://api.telegram.org/"

        f"bot{TELEGRAM_TOKEN}/sendMessage"

    )



    requests.post(

        url,

        json={

            "chat_id":
            CHAT_ID,

            "text":
            message

        }

    )





# --------------------------------------------------
# START
# --------------------------------------------------

matches = get_atp_matches()



if matches["status"] == "empty":


    send_telegram(

        matches["message"]

    )


    print(

        "Nėra ATP TOP lygio mačų"

    )


    exit()





prediction = analyze(

    matches["matches"]

)





save_history(

    prediction

)





telegram_message = (

    "🎾 ATP DAILY VALUE PICKS\n\n"

    + prediction

)





send_telegram(

    telegram_message

)





print(

    "ATP value prognozė išsiųsta"

)
