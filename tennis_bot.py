import os
from datetime import datetime
import requests

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get(
    "ODDS_API_KEY"
)


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






def extract_odds(event):

    odds = {}


    markets = event.get(
        "markets",
        []
    )


    for market in markets:

        outcomes = market.get(
            "outcomes",
            []
        )


        for outcome in outcomes:

            name = outcome.get(
                "name"
            )


            price = outcome.get(
                "price"
            )


            if name and price:

                odds[name] = price



    return odds






def attach_odds(matches, events):


    if matches.get("status") == "empty":

        return matches



    for match in matches["matches"]:


        player1 = match["player1"]["name"]

        player2 = match["player2"]["name"]


        found_odds = {}



        for event in events:


            event_text = str(event).lower()


            if (
                player1.lower() in event_text
                and
                player2.lower() in event_text
            ):

                found_odds = extract_odds(
                    event
                )

                break



        match["odds"] = found_odds



    return matches







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


        return






    for match in matches["matches"]:



        odds = match.get(
            "odds",
            {}
        )



        if not odds:

            continue



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
            odds
        )


        print(
            "STATUS: READY FOR ANALYSIS"
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




    print_events(
        events
    )



    matches = get_atp_matches(
        events
    )



    matches = attach_odds(
        matches,
        events
    )



    generate_value_report(
        matches
    )






if __name__ == "__main__":

    main()
