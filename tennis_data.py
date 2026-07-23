from datetime import datetime


def is_valid_atp_event(event):

    league = event.get("league", {})

    name = league.get("name", "").lower()


    if "doubles" in name:
        return False


    if "atp" in name:
        return True


    if "challenger" in name:
        return True


    return False




def get_atp_matches(events):

    today = datetime.now().strftime("%Y-%m-%d")


    matches = []


    for event in events:


        if not is_valid_atp_event(event):
            continue



        league = event.get(
            "league",
            {}
        )


        tournament = league.get(
            "name",
            "Unknown"
        )



        home = event.get(
            "home"
        )


        away = event.get(
            "away"
        )


        if not home or not away:
            continue



        matches.append({

            "date": today,

            "event_id": event.get("id"),

            "tournament": tournament,


            "player1": {

                "name": home

            },


            "player2": {

                "name": away

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
