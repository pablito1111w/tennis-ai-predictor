import os
import requests
from datetime import datetime


ODDS_API_KEY = os.environ["ODDS_API_KEY"]



# Tik šitie turnyrai
ALLOWED_KEYWORDS = [

    "atp 500",
    "atp masters",
    "masters 1000",
    "grand slam",
    "wimbledon",
    "us open",
    "australian open",
    "roland garros",
    "french open"

]



# ---------------------------------------------
# GAUNAM VISUS TENISO EVENTUS
# ---------------------------------------------

def get_events():


    url = "https://api.odds-api.io/v3/events"



    params = {

        "apiKey": ODDS_API_KEY,

        "sport": "tennis",

        "status": "pending"

    }



    try:


        response = requests.get(

            url,

            params=params,

            timeout=30

        )


        response.raise_for_status()


        data = response.json()



        if isinstance(data, list):

            return data



        return data.get(
            "events",
            []
        )



    except Exception as e:


        print(
            "Events API klaida:",
            e
        )


        return []





# ---------------------------------------------
# PATIKRINAM TURNYRĄ
# ---------------------------------------------

def is_allowed_tournament(name):


    if not name:

        return False



    name = name.lower()



    for word in ALLOWED_KEYWORDS:


        if word in name:

            return True



    return False





# ---------------------------------------------
# ATP MAČAI
# ---------------------------------------------

def get_atp_matches():


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )



    events = get_events()



    matches = []



    print(
        "===== TENNIS EVENTS ====="
    )



    for event in events:



        league = event.get(
            "league",
            {}
        )



        if isinstance(
            league,
            dict
        ):

            tournament = league.get(
                "name",
                ""
            )

        else:

            tournament = str(
                league
            )



        print(
            "TOURNAMENT:",
            tournament
        )



        if not is_allowed_tournament(
            tournament
        ):

            continue




        home = event.get(
            "home",
            event.get(
                "home_team",
                "Unknown"
            )
        )



        away = event.get(
            "away",
            event.get(
                "away_team",
                "Unknown"
            )
        )



        odds = event.get(
            "odds",
            {}
        )



        if not odds:

            odds = event.get(
                "bookmakers",
                {}
            )



        print(
            "MATCH:",
            home,
            "vs",
            away
        )


        print(
            "ODDS:",
            odds
        )





        matches.append(

            {

                "date":
                today,


                "event_id":
                event.get(
                    "id"
                ),


                "tournament":
                tournament,


                "player1":
                {

                    "name":
                    home

                },


                "player2":
                {

                    "name":
                    away

                },


                "odds":
                odds,


                "h2h":
                "unknown",


                "ranking":
                "unknown",


                "form":
                "unknown"

            }

        )



    print(
        "===== END EVENTS ====="
    )



    if len(matches) == 0:


        return {

            "status":
            "empty",


            "message":
            "🎾 Šiandien nėra ATP 500 / Masters 1000 / Grand Slam mačų"

        }



    return {

        "status":
        "ok",


        "matches":
        matches

    }
