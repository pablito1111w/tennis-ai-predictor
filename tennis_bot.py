import os
import requests

from tennis_data import get_atp_matches


ODDS_API_KEY = os.environ.get(
    "ODDS_API_KEY"
)



def get_events():


    url = "https://api.odds-api.io/v3/events"


    params = {

        "apiKey":ODDS_API_KEY,

        "sport":"tennis",

        "status":"pending"

    }


    r = requests.get(
        url,
        params=params,
        timeout=20
    )


    r.raise_for_status()


    data = r.json()


    if isinstance(data,list):

        return data


    return []





def get_market_odds(event):


    result = {}


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

                result[name]=price



    return result







def add_odds(matches,events):


    for match in matches["matches"]:


        eid = match["event_id"]


        for event in events:


            if event.get("id")==eid:


                match["odds"]=get_market_odds(event)

                break



    return matches







def report(matches):


    print()

    print(
        "🎾 ATP DAILY VALUE PICKS"
    )

    print(
        "------------------------"
    )



    counter=0



    for m in matches["matches"]:


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



        if m["odds"]:


            print(
                "ODDS:",
                m["odds"]
            )


        else:

            print(
                "ODDS: NO DATA"
            )



        print(
            "----------------"
        )


        counter+=1



    print()

    print(
        "TOTAL MATCHES:",
        counter
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


    matches=add_odds(
        matches,
        events
    )


    report(
        matches
    )




if __name__=="__main__":

    main()
