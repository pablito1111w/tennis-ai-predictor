import os
from datetime import datetime

import requests


ODDS_API_KEY = os.environ["ODDS_API_KEY"]



# --------------------------------------------------
# GET EVENTS FROM ODDS API
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
            str(e)
        )

        return []




# --------------------------------------------------
# ATP TOP TURNYRŲ FILTRAS
# --------------------------------------------------

def is_top_atp_tournament(league_name):


    name = league_name.lower()



    # pašalinam nereikalingus

    banned = [

        "wta",
        "women",
        "doubles",
        "double",
        "challenger",
        "itf",
        "utr",
        "qualifier",
        "qualification"

    ]


    for word in banned:

        if word in name:

            return False




    # paliekam tik ATP TOP

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

        word in name

        for word in allowed

    )




# --------------------------------------------------
# ATP MATCHES
# --------------------------------------------------

def get_atp_matches():


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    events = get_events()



    print(
        "\n===== TENNIS EVENTS ====="
    )


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




        print(
            "TOURNAMENT:",
            tournament
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



        match = {


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

            event.get(
                "odds",
                {}
            ),



            "h2h":
            "unknown"


        }



        matches.append(
            match
        )




    print(
        "===== END EVENTS =====\n"
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
