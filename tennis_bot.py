import os
import requests
from datetime import datetime

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get("ODDS_API_KEY")


def get_events():

    url = "https://api.odds-api.io/v3/events"

    params = {
        "apiKey": ODDS_API_KEY,
        "sport": "tennis",
        "status": "pending"
    }

    try:

        r = requests.get(
            url,
            params=params,
            timeout=20
        )

        r.raise_for_status()

        data = r.json()

        if isinstance(data, list):
            return data

        return []

    except Exception as e:

        print("API ERROR:", e)
        return []




def normalize_name(name):

    if not name:
        return ""

    return (
        name.lower()
        .replace(".", "")
        .replace("-", "")
        .replace(" ", "")
    )




def find_event_odds(match, events):


    p1 = normalize_name(
        match["player1"]["name"]
    )

    p2 = normalize_name(
        match["player2"]["name"]
    )


    for event in events:


        text = normalize_name(
            str(event)
        )


        if p1 in text and p2 in text:


            # PARODOM VISA STRUKTŪRĄ JEIGU RANDAM
            # print(event)


            odds = {}


            if "odds" in event:

                odds = event["odds"]


            elif "markets" in event:


                for market in event["markets"]:


                    for outcome in market.get("outcomes", []):


                        name = outcome.get(
                            "name"
                        )

                        price = outcome.get(
                            "price"
                        )


                        if name and price:

                            odds[name] = price



            return odds



    return {}





def generate_report(matches):


    print()
    print("🎾 ATP DAILY VALUE PICKS")
    print("------------------------")


    count = 0


    for match in matches["matches"]:


        odds = match.get(
            "odds",
            {}
        )


        print()

        print(
            "TOURNAMENT:",
            match["tournament"]
        )


        print(
            match["player1"]["name"],
            "vs",
            match["player2"]["name"]
        )


        if odds:

            print(
                "ODDS:",
                odds
            )

        else:

            print(
                "ODDS: NO DATA"
            )


        print(
            "----------------"
        )


        count += 1



    print()

    print(
        "TOTAL MATCHES:",
        count
    )







def main():


    print(
        "Paleidžiama ATP analizė..."
    )


    events = get_events()


    print(
        "Gauta įvykių:",
        len(events)
    )


    matches = get_atp_matches(
        events
    )



    if matches["status"] == "empty":

        print(
            "Nėra ATP mačų"
        )

        return




    for match in matches["matches"]:


        match["odds"] = find_event_odds(
            match,
            events
        )




    generate_report(
        matches
    )





if __name__ == "__main__":

    main()
