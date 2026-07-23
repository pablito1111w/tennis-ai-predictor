from datetime import datetime



def is_top_atp_tournament(league_name):

    if not league_name:
        return False


    name = league_name.lower()


    if "doubles" in name:
        return False


    if "atp" in name:
        return True


    grand_slams = [

        "wimbledon",
        "us open",
        "australian open",
        "roland garros",
        "french open"

    ]


    for item in grand_slams:

        if item in name:
            return True


    return False






def extract_event_odds(event):


    odds = {}



    # kai kurie API variantai
    if "odds" in event:

        return event["odds"]



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


            player = outcome.get(
                "name"
            )


            price = outcome.get(
                "price"
            )


            if player and price:


                odds[player] = price



    return odds







def get_atp_matches(events):


    today = datetime.now().strftime(
        "%Y-%m-%d"
    )


    matches = []



    for event in events:



        league = event.get(
            "league",
            {}
        )


        tournament = league.get(
            "name",
            "Unknown Tournament"
        )



        if not is_top_atp_tournament(
            tournament
        ):

            continue





        home = event.get(
            "home",
            event.get(
                "home_team",
                "Unknown"
            )
        )



        away = event.get(
            "away",
            event.get(
                "away_team",
                "Unknown"
            )
        )



        odds = extract_event_odds(
            event
        )




        match = {


            "date":
            today,



            "event_id":
            event.get(
                "id"
            ),



            "tournament":
            tournament,



            "player1":
            {

                "name":
                home,

                "ranking":
                "unknown",

                "form":
                "unknown"

            },



            "player2":
            {

                "name":
                away,

                "ranking":
                "unknown",

                "form":
                "unknown"

            },



            "odds":
            odds,



            "h2h":
            "unknown"

        }



        matches.append(
            match
        )






    if len(matches) == 0:


        return {


            "status":
            "empty",



            "message":
            "🎾 Šiandien nėra ATP mačų su pakankamais duomenimis VALUE analizei"

        }







    return {


        "status":
        "ok",



        "matches":
        matches

    }
