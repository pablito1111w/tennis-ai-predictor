import os
import requests

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get("ODDS_API_KEY")

BASE_URL = "https://api.odds-api.io/v3"


def get_events():

    url = f"{BASE_URL}/events"

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

        return data if isinstance(data, list) else []


    except Exception as e:

        print("EVENT ERROR:", e)
        return []



def get_odds():

    url = f"{BASE_URL}/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "sport": "tennis"
    }


    try:

        r = requests.get(
            url,
            params=params,
            timeout=20
        )


        r.raise_for_status()


        data = r.json()


        return data if isinstance(data, list) else []


    except Exception as e:

        print("ODDS ERROR:", e)
        return []





def normalize(x):

    if not x:
        return ""

    return (
        str(x)
        .lower()
        .replace(" ","")
        .replace(".","")
        .replace("-","")
        .replace(",","")
        .replace("'","")
    )





def find_odds(match, odds_data):


    p1 = normalize(
        match["player1"]["name"]
    )

    p2 = normalize(
        match["player2"]["name"]
    )


    for odd in odds_data:


        text = normalize(
            odd
        )


        if p1 in text and p2 in text:


            return extract_prices(
                odd
            )


    return {}






def extract_prices(data):


    result = {}


    if not isinstance(data, dict):

        return result



    markets = data.get(
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

                result[name] = price



    return result







def report(matches):


    print()
    print("🎾 ATP DAILY VALUE PICKS")
    print("------------------------")


    total = 0


    for m in matches["matches"]:


        odds = m.get(
            "odds",
            {}
        )


        if not odds:
            continue



        print()

        print(
            "TOURNAMENT:",
            m["tournament"]
        )


        print(
            m["player1"]["name"],
            "vs",
            m["player2"]["name"]
        )


        print(
            "ODDS:",
            odds
        )


        print("----------------")


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


    odds_data = get_odds()


    print(
        "Gauta odds įrašų:",
        len(odds_data)
    )



    found = 0



    for match in matches["matches"]:


        odds = find_odds(
            match,
            odds_data
        )


        match["odds"] = odds


        if odds:
            found += 1




    print(
        "Rasta koeficientų:",
        found
    )


    report(
        matches
    )






if __name__ == "__main__":

    main()
