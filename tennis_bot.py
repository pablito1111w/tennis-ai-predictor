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

        print(
            "EVENT ERROR:",
            e
        )

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






def get_event_odds(event_id):


    url = f"{BASE_URL}/odds"


    params = {

        "apiKey": ODDS_API_KEY,

        "eventId": event_id

    }


    try:


        r = requests.get(

            url,

            params=params,

            timeout=20

        )


        if r.status_code != 200:

            return {}



        data = r.json()



        odds = {}



        if isinstance(data, dict):


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

                        odds[name] = price



        return odds



    except Exception:


        return {}







def find_event(match, events):


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


            return event



    return None







def report(matches):


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


        event = find_event(
            match,
            events
        )


        if not event:


            match["odds"] = {}

            continue




        event_id = event.get(
            "id"
        )


        odds = get_event_odds(
            event_id
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
