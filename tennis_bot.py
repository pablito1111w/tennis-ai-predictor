import os
import time
import requests

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get("ODDS_API_KEY")

BASE_URL = "https://api.odds-api.io/v3"

ODDS_CACHE = {}





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


        return data if isinstance(data,list) else []



    except Exception as e:

        print(
            "EVENT ERROR:",
            e
        )

        return []







def get_event_odds(event_id):


    if event_id in ODDS_CACHE:

        return ODDS_CACHE[event_id]



    url = f"{BASE_URL}/odds"


    params = {

        "apiKey": ODDS_API_KEY,

        "eventId": event_id

    }



    for attempt in range(3):


        try:


            # apsauga nuo rate limit

            time.sleep(2)



            r = requests.get(

                url,

                params=params,

                timeout=20

            )



            if r.status_code == 429:


                print(
                    "API LIMIT - laukiu..."
                )


                time.sleep(15)

                continue



            if r.status_code != 200:


                return {}



            data = r.json()


            odds = {}



            if isinstance(data,dict):


                markets=data.get(
                    "markets",
                    []
                )



                for market in markets:


                    for outcome in market.get(
                        "outcomes",
                        []
                    ):


                        name=outcome.get(
                            "name"
                        )


                        price=outcome.get(
                            "price"
                        )


                        if name and price:

                            odds[name]=price



            elif isinstance(data,list):


                for item in data:


                    if not isinstance(item,dict):

                        continue



                    for market in item.get(
                        "markets",
                        []
                    ):


                        for outcome in market.get(
                            "outcomes",
                            []
                        ):


                            name=outcome.get(
                                "name"
                            )


                            price=outcome.get(
                                "price"
                            )


                            if name and price:

                                odds[name]=price




            ODDS_CACHE[event_id]=odds


            return odds




        except Exception as e:


            print(
                "ODDS ERROR:",
                e
            )


            time.sleep(5)



    return {}









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








def find_event(match,events):


    p1=normalize(
        match["player1"]["name"]
    )


    p2=normalize(
        match["player2"]["name"]
    )



    for event in events:


        home=normalize(
            event.get("home")
        )


        away=normalize(
            event.get("away")
        )



        if (

            p1 in home and p2 in away

        ) or (

            p2 in home and p1 in away

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


    total=0



    for m in matches["matches"]:


        odds=m.get(
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


        print(
            "----------------"
        )


        total+=1




    print()

    print(
        "TOTAL WITH ODDS:",
        total
    )









def main():


    print(
        "Paleidžiama ATP analizė..."
    )



    events=get_events()



    print(
        "Gauta įvykių:",
        len(events)
    )



    matches=get_atp_matches(
        events
    )



    found=0



    # tik realūs ATP/challenger mačai

    for match in matches["matches"]:


        event=find_event(
            match,
            events
        )



        if not event:


            match["odds"]={}

            continue



        odds=get_event_odds(
            event.get("id")
        )



        match["odds"]=odds



        if odds:

            found+=1






    print(
        "Rasta koeficientų:",
        found
    )



    report(
        matches
    )







if __name__=="__main__":

    main()
