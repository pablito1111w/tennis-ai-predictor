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







def get_odds(event_id):


    if not event_id:

        return {}



    url = "https://api.odds-api.io/v3/odds"



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


        r.raise_for_status()


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




    except Exception as e:


        print(
            "ODDS ERROR:",
            e
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



        odds = match.get(
            "odds",
            {}
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



        total += 1




    print()

    print(
        "TOTAL MATCHES:",
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





    for match in matches["matches"]:


        match["odds"] = get_odds(

            match["event_id"]

        )





    generate_report(
        matches
    )







if __name__ == "__main__":

    main()
