import os
import requests
from datetime import datetime


ODDS_API_KEY = os.environ["ODDS_API_KEY"]


ALLOWED_TOURNAMENTS = [
    "ATP 500",
    "ATP Masters 1000",
    "Grand Slam"
]



def get_odds_matches():

    url = "https://api.odds-api.io/v3/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "sport": "tennis",
        "region": "eu"
    }


    response = requests.get(
        url,
        params=params,
        timeout=20
    )


    if response.status_code != 200:

        print(
            "Odds API klaida:",
            response.text
        )

        return []



    return response.json()




def get_atp_matches():

    today = datetime.now().strftime("%Y-%m-%d")


    odds_data = get_odds_matches()


    matches = []


    for game in odds_data:


        tournament = game.get(
            "league",
            ""
        )


        if not any(
            x in tournament
            for x in ALLOWED_TOURNAMENTS
        ):
            continue



        matches.append(

            {
                "date": today,

                "tournament": tournament,


                "player1": {
                    "name":
                    game["home_team"],

                    "ranking":
                    "unknown",

                    "form":
                    "unknown",

                    "serve_rating":
                    "unknown",

                    "return_rating":
                    "unknown"
                },


                "player2": {
                    "name":
                    game["away_team"],

                    "ranking":
                    "unknown",

                    "form":
                    "unknown",

                    "serve_rating":
                    "unknown",

                    "return_rating":
                    "unknown"
                },


                "h2h":
                "reikia papildyti",


                "odds": {

                    "player1":
                    game.get(
                        "home_odds",
                        None
                    ),

                    "player2":
                    game.get(
                        "away_odds",
                        None
                    )
                }
            }

        )



    if len(matches) == 0:

        return {

            "status": "empty",

            "message":
            "🎾 Šiandien nėra tinkamų ATP TOP lygio mačų"

        }



    return {

        "status": "ok",

        "matches": matches

    }
