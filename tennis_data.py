from datetime import datetime


def is_top_atp_tournament(league_name):

    if not league_name:
        return False

    name = league_name.lower()


    # išmetam dvejetus
    if "doubles" in name:
        return False


    # ATP pagrindiniai
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





def get_player(event, side):

    possible = [

        event.get(side),

        event.get(
            "participants",
            {}
        ).get(side),

    ]


    for item in possible:

        if item:
            return item


    return "Unknown"





def get_atp_matches(events):


    today = datetime.now().strftime("%Y-%m-%d")


    matches = []



    for event in events:


        league = event.get(
            "league",
            {}
        )


        tournament = league.get(
            "name",
            ""
        )


        if not is_top_atp_tournament(tournament):

            continue



        home = get_player(
            event,
            "home"
        )


        away = get_player(
            event,
            "away"
        )



        # jei API naudoja kitus laukus

        if home == "Unknown":

            home = event.get(
                "home_team",
                "Unknown"
            )



        if away == "Unknown":

            away = event.get(
                "away_team",
                "Unknown"
            )




        if home == "Unknown" or away == "Unknown":

            continue





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
                home

            },



            "player2":
            {

                "name":
                away

            },



            "odds":
            event.get(
                "odds",
                {}
            )

        }



        matches.append(
            match
        )





    print(
        "ATP MATCHES FOUND:",
        len(matches)
    )



    if not matches:


        return {

            "status":
            "empty",


            "matches":
            []

        }



    return {


        "status":
        "ok",


        "matches":
        matches

    }
