import os
import requests
from openai import OpenAI


# Gauname slaptažodžius iš GitHub Secrets
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
OPENAI_KEY = os.environ["OPENAI_KEY"]


client = OpenAI(api_key=OPENAI_KEY)


# Kol kas testiniai mačai.
# Vėliau čia prijungsime realius ATP/WTA mačus.
def get_matches():

    return """
    Šiandienos teniso mačai:

    ATP:
    Jannik Sinner - Daniil Medvedev
    Carlos Alcaraz - Casper Ruud

    WTA:
    Iga Swiatek - Coco Gauff
    """



def analyze(matches):

    prompt = f"""
Tu esi profesionalus teniso analitikas.

Išanalizuok šiuos mačus:

{matches}

Analizei naudok:
- dabartinę žaidėjų formą
- paskutinių mačų rezultatus
- žaidimo stilių
- dangos tinkamumą
- tarpusavio istoriją (H2H)

Pateik:

1. Tikėtiną nugalėtoją
2. Galimą setų rezultatą
3. Galimą over/under pasirinkimą
4. Pasitikėjimą procentais
5. Trumpą argumentaciją

Rinkis tik stipriausias prognozes.
Nerašyk bereikalingų pasirinkimų.
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



def send_telegram(message):

    url = (
        f"https://api.telegram.org/"
        f"bot{TELEGRAM_TOKEN}/sendMessage"
    )


    data = {
        "chat_id": CHAT_ID,
        "text": message
    }


    requests.post(
        url,
        json=data
    )



# Paleidimas

matches = get_matches()

prediction = analyze(matches)


telegram_message = (
    "🎾 DIENOS TENISO ANALIZĖ\n\n"
    + prediction
)


send_telegram(telegram_message)


print("Prognozė išsiųsta į Telegram")
