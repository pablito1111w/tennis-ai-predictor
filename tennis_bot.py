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

                print("API LIMIT - waiting...")

                time.sleep(10)

                continue



            r.raise_for_status()

            return r.json()



        except Exception as e:

            print(
                "API ERROR:",
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








def get_all_odds():


    data = api_get(

        f"{BASE_URL}/odds",

        {
            "apiKey": ODDS_API_KEY
        }

    )


    if isinstance(data,list):

        return data



    if isinstance(data,dict):

        return data.get(
            "events",
            []
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







def extract_odds(item):


    result = {}



    if not isinstance(item,dict):

        return result



    markets = item.get(
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

                result[name]=price



    return result







def match_odds(match, odds):


    p1 = normalize(
        match["player1"]["name"]
    )


    p2 = normalize(
        match["player2"]["name"]
    )



    for item in odds:


        text = normalize(
            str(item)
        )



        if p1 in text and p2 in text:


            return extract_odds(
                item
            )


    return {}









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



    if not events:

        print(
            "API neduoda events"
        )

        return





    matches=get_atp_matches(
        events
    )



    odds=get_all_odds()



    print(
        "Gauta odds:",
        len(odds)
    )



    found=0



    for match in matches["matches"]:


        value=match_odds(
            match,
            odds
        )


        match["odds"]=value



        if value:

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
