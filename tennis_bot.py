import os
import requests

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





def normalize(name):

    if not name:
        return ""

    return (
        str(name)
        .lower()
        .replace(" ", "")
        .replace(".", "")
        .replace("-", "")
        .replace(",", "")
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






def find_odds(match, events):


    p1 = normalize(
        match["player1"]["name"]
    )

    p2 = normalize(
        match["player2"]["name"]
    )



    for event in events:


        home = normalize(
            event.get("home")
        )


        away = normalize(
            event.get("away")
        )



        if (

            (p1 in home and p2 in away)

            or

            (p2 in home and p1 in away)

        ):


            return extract_odds(
                event
            )



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
