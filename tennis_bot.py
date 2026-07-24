import os
import time
import requests

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get("ODDS_API_KEY")

BASE_URL = "https://api.odds-api.io/v3"


HEADERS = {
    "User-Agent": "tennis-value-bot"
}




def api_get(url, params):

    for attempt in range(3):

        try:

            r = requests.get(
                url,
                params=params,
                headers=HEADERS,
                timeout=20
            )


            if r.status_code == 429:

                print("API LIMIT - laukiam...")
                time.sleep(15)
                continue



            if r.status_code != 200:

                print(
                    "API ERROR:",
                    r.status_code,
                    r.text[:300]
                )

                return None



            return r.json()



        except Exception as e:

            print(
                "REQUEST ERROR:",
                e
            )

            time.sleep(5)



    return None






def get_events():

    data = api_get(

        f"{BASE_URL}/events",

        {
            "apiKey": ODDS_API_KEY,
            "sport": "tennis",
            "status": "pending"
        }

    )


    if isinstance(data,list):

        return data


    return []







def get_event_odds(event_id):


    data = api_get(

        f"{BASE_URL}/odds",

        {
            "apiKey": ODDS_API_KEY,
            "eventId": event_id
        }

    )


    odds = {}



    if isinstance(data,dict):


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



    elif isinstance(data,list):


        for market in data:


            if not isinstance(market,dict):

                continue


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







def normalize(name):

    if not name:

        return ""


    return (

        str(name)
        .lower()
        .replace(" ","")
        .replace(".","")
        .replace("-","")
        .replace(",","")
        .replace("'","")

    )







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

            p1 in home
            and
            p2 in away

        ) or (

            p2 in home
            and
            p1 in away

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



    if not events:


        print(
            "API neduoda events"
        )

        return




    matches = get_atp_matches(
        events
    )



    found = 0



    checked = 0



    for match in matches["matches"]:


        event = find_event(
            match,
            events
        )


        if not event:

            match["odds"] = {}

            continue



        checked += 1



        odds = get_event_odds(
            event.get("id")
        )


        match["odds"] = odds



        if odds:

            found += 1



        # apsauga nuo limito
        time.sleep(1)





    print(
        "Patikrinta event:",
        checked
    )


    print(
        "Rasta koeficientų:",
        found
    )



    report(
        matches
    )







if __name__ == "__main__":

    main()
