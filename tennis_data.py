import requests
from datetime import datetime


def get_atp_matches():

    """
    Kol kas duomenų sluoksnio testas.
    Čia vėliau jungsime realius ATP 500/1000/Grand Slam mačus.
    """

    today = datetime.now().strftime("%Y-%m-%d")

    matches = [

        {
            "date": today,
            "tournament": "ATP Masters 1000",
            "surface": "Hard",
            "player1": "Jannik Sinner",
            "player2": "Daniil Medvedev",
            "ranking1": 1,
            "ranking2": 5,
            "form1": "8/10",
            "form2": "6/10",
            "h2h": "Sinner leads 6-5",
            "odds1": 1.55,
            "odds2": 2.60
        },

        {
            "date": today,
            "tournament": "ATP 500",
            "surface": "Clay",
            "player1": "Carlos Alcaraz",
            "player2": "Casper Ruud",
            "ranking1": 2,
            "ranking2": 8,
            "form1": "9/10",
            "form2": "7/10",
            "h2h": "Alcaraz leads 4-1",
            "odds1": 1.40,
            "odds2": 3.00
        }

    ]

    return matches
