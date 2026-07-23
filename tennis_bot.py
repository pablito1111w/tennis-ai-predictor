import os
import requests
import json

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


        print(
            "EVENTS ERROR:",
            e
        )


        return []






def normalize(value):


    if not value:

        return ""


    return (

        str(value)
        .lower()
        .replace(" ", "")
        .replace(".", "")
        .replace("-", "")
        .replace(",", "")
        .replace("'", "")

    )







def extract_odds(event):


    odds = {}



    # tiesioginis odds

    if isinstance(event.get("odds"), dict):

        return event["odds"]



    # markets struktūra

    markets = event.get(
        "markets",
        []
    )



    for market in markets:


        for outcome in market.get(
            "outcomes",
            []
        ):


            name = outcome.get(
                "name"
            )


            price = outcome.get(
                "price"
            )


            if name and price:

                odds[name] = price



    return odds







def find_odds(match, events):


    p1 = normalize(
        match["player1"]["name"]
    )


    p2 = normalize(
        match["player2"]["name"]
    )



    for event in events:


        text = normalize(
            json.dumps(event)
        )



        if p1 in text and p2 in text:


            odds = extract_odds(
                event
            )


            return odds



    return {}







def generate_report(matches):


    print()

    print(
        "🎾 ATP DAILY VALUE PICKS"
    )

    print(
        "------------------------"
    )



    total = 0



    for match in matches["matches"]:


        odds = match.get(
            "odds",
            {}
        )


        if not odds:

            continue



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


        print(
            "ODDS:",
            odds
        )


        print(
            "----------------"
        )


        total += 1



    print()

    print(
        "TOTAL WITH ODDS:",
        total
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



    if events:


        print(
            "\nDEBUG FIRST EVENT KEYS:"
        )


        print(
            events[0].keys()
        )



    matches = get_atp_matches(
        events
    )



    if matches["status"] == "empty":


        print(
            "Nėra ATP mačų"
        )


        return






    found = 0



    for match in matches["matches"]:



        odds = find_odds(

            match,

            events

        )



        match["odds"] = odds



        if odds:

            found += 1






    print(

        "Rasta koeficientų:",

        found

    )



    generate_report(
        matches
    )







if __name__ == "__main__":

    main()
