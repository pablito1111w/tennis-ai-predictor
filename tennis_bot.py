import os
import json
from datetime import datetime

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get(
    "ODDS_API_KEY"
)



def get_events():

    import requests


    url = "https://api.odds-api.io/v3/events"


    params = {

        "apiKey":
        ODDS_API_KEY,

        "sport":
        "tennis",

        "status":
        "pending"
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





def print_events(events):


    print(
        "===== TENNIS EVENTS ====="
    )


    for event in events:


        league = event.get(
            "league",
            {}
        )


        name = league.get(
            "name",
            "Unknown"
        )


        print(
            "TOURNAMENT:",
            name
        )



    print(
        "===== END EVENTS ====="
    )






def generate_value_report(matches):


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    print()

    print(
        "🎾 ATP DAILY VALUE PICKS"
    )

    print()

    print(
        "🎾 TOP ATP VALUE PICKS OF THE DAY"
    )

    print()


    if matches.get("status") == "empty":


        print(
            f"Šiandien ({today}) nėra ATP mačų su pakankamais duomenimis VALUE analizei."
        )

        print()

        print(
            "STATUS: NO ODDS DATA"
        )

        print()

        print(
            "================="
        )

        return



    for match in matches["matches"]:


        print(
            "TOURNAMENT:",
            match["tournament"]
        )


        print(
            match["player1"]["name"],
            "vs",
            match["player2"]["name"]
        )


        print(
            "ODDS:",
            match["odds"]
        )


        print(
            "STATUS: NEED ANALYSIS"
        )


        print(
            "---------------------"
        )







def main():


    print(
        "Paleidžiama ATP analizė..."
    )


    events = get_events()



    if not events:


        print(
            "Nerasta įvykių"
        )

        return




    # parodyti visus API turnyrus loge

    print_events(
        events
    )



    # SVARBUS PAKEITIMAS
    # perduodam events į get_atp_matches()

    matches = get_atp_matches(
        events
    )



    generate_value_report(
        matches
    )







if __name__ == "__main__":


    main()
