from datetime import datetime



def is_valid_tournament(name):

    if not name:
        return False


    n = name.lower()


    # išmetam nereikalingus
    if "doubles" in n:
        return False


    if "utr" in n:
        return False


    if "itf" in n:
        return False


    # paliekam ATP ir Challenger
    if "atp" in n:
        return True


    if "challenger" in n:
        return True


    return False






def clean_player(name):

    if not name:
        return False


    bad_names = [

        "qf",
        "r16",
        "r32",
        "r64",
        "wqf",
        "wsf",
        "winner",
        "loser",
        "qualifier",
        "tbd"

    ]


    n = str(name).lower()


    for bad in bad_names:

        if bad in n:

            return False



    return True







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
            ""
        )



        if not is_valid_tournament(
            tournament
        ):

            continue





        home = event.get(
            "home"
        )


        away = event.get(
            "away"
        )



        if not clean_player(home):

            continue



        if not clean_player(away):

            continue




        matches.append({


            "date": today,


            "event_id": event.get(
                "id"
            ),



            "tournament": tournament,



            "player1": {

                "name": home

            },



            "player2": {

                "name": away

            },



            "odds": {}



        })






    if len(matches) == 0:


        return {


            "status": "empty",


            "matches": []

        }







    return {


        "status": "ok",


        "matches": matches

    }
