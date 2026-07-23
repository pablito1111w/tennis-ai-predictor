from datetime import datetime


def is_valid_tournament(name):

    if not name:
        return False

    n = name.lower()


    if "doubles" in n:
        return False


    if "utr" in n:
        return False


    if "itf" in n:
        return False


    if "atp" in n:
        return True


    if "challenger" in n:
        return True


    return False




def clean_player(name):

    if not name:
        return False


    bad = [
        "qf",
        "r16",
        "r32",
        "wqf",
        "wsf",
        "winner",
        "loser"
    ]


    low = name.lower()


    for b in bad:

        if b in low:
            return False


    return True





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



        if not is_valid_tournament(tournament):

            continue



        player1 = event.get(
            "home"
        )


        player2 = event.get(
            "away"
        )



        if not clean_player(player1):

            continue


        if not clean_player(player2):

            continue



        matches.append({

            "date": today,

            "event_id": event.get("id"),

            "tournament": tournament,


            "player1": {

                "name": player1

            },


            "player2": {

                "name": player2

            },


            "odds": {}

        })




    if not matches:

        return {

            "status":"empty",

            "matches":[]

        }



    return {

        "status":"ok",

        "matches":matches

    }
