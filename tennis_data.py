import os
from datetime import datetime

import requests


ODDS_API_KEY = os.environ["ODDS_API_KEY"]



# --------------------------------------------------
# GET EVENTS
# --------------------------------------------------

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
            timeout=20
        )

        response.raise_for_status()

        data = response.json()


        if isinstance(data, list):
            return data


        return []


    except Exception as e:

        print(
            "Odds API klaida:",
            e
        )

        return []




# --------------------------------------------------
# ATP FILTRAS
# --------------------------------------------------

def is_top_atp_tournament(name):

    name = name.lower()


    banned = [

        "wta",
        "women",
        "doubles",
        "double",
        "challenger",
        "itf",
        "utr",
        "qualifier"

    ]


    for x in banned:

        if x in name:

            return False



    allowed = [

        "atp",
        "masters",
        "grand slam",
        "wimbledon",
        "us open",
        "australian open",
        "roland garros",
        "french open"

    ]


    return any(
        x in name
        for x in allowed
    )




# --------------------------------------------------
# ATP MATCHES
# --------------------------------------------------

def get_atp_matches():

    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    events = get_events()


    matches = []



    for event in events:


        league = event.get(
            "league",
            {}
        )


        if isinstance(league, dict):

            tournament = league.get(
                "name",
                ""
            )

        else:

            tournament = str(
                league
            )



        if not is_top_atp_tournament(
            tournament
        ):

            continue



        home = event.get(
            "home",
            "Unknown"
        )


        away = event.get(
            "away",
            "Unknown"
        )



        odds = event.get(
            "odds",
            {}
        )


        print(
            "ATP:",
            tournament,
            home,
            "vs",
            away
        )


        print(
            "ODDS:",
            odds
        )



        match = {


            "date":
            today,


            "tournament":
            tournament,


            "player1":
            {

                "name":
                home,

                "ranking":
                "unknown",

                "form":
                "unknown"

            },


            "player2":
            {

                "name":
                away,

                "ranking":
                "unknown",

                "form":
                "unknown"

            },


            "odds":
            odds,


            "h2h":
            "unknown"

        }



        matches.append(
            match
        )




    if not matches:


        return {

            "status":
            "empty",

            "message":
            "🎾 Šiandien nėra ATP TOP lygio mačų"

        }



    return {

        "status":
        "ok",

        "matches":
        matches

    }
