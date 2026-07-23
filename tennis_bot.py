import os
import requests

from tennis_data import get_atp_matches



ODDS_API_KEY = os.environ.get(
    "ODDS_API_KEY"
)




def get_events():


    url = "https://api.odds-api.io/v3/events"



    params = {

        "apiKey": ODDS_API_KEY,

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



    return data if isinstance(data,list) else []






def extract_odds(event):


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






def match_odds(match,events):


    p1 = match["player1"]["name"].lower()

    p2 = match["player2"]["name"].lower()



    for event in events:


        text = str(event).lower()



        if p1 in text and p2 in text:


            return extract_odds(event)



    return {}








def generate_report(matches):


    print("\n🎾 ATP DAILY VALUE PICKS\n")



    if matches["status"]=="empty":


        print(
            "Nėra ATP mačų"
        )

        return




    count=0



    for m in matches["matches"]:


        odds=m.get(
            "odds"
        )



        print(
            "--------------------------------"
        )


        print(
            "TOURNAMENT:",
            m["tournament"]
        )


        print(
            m["player1"]["name"],
            "vs",
            m["player2"]["name"]
        )



        if odds:


            print(
                "ODDS:",
                odds
            )


            print(
                "STATUS: READY"
            )


        else:


            print(
                "ODDS: NOT FOUND"
            )


        count+=1




    print(
        "\nTOTAL MATCHES:",
        count
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




    for m in matches.get("matches",[]):


        m["odds"]=match_odds(
            m,
            events
        )



    generate_report(
        matches
    )







if __name__=="__main__":

    main()
