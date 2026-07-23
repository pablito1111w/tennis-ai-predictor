from datetime import datetime


def is_top_atp_tournament(league_name):

    if not league_name:
        return False


    name = league_name.lower()


    # atmetam dvejetus
    if "doubles" in name:
        return False


    # ATP pagrindiniai turnyrai
    if "atp" in name:
        return True


    # Grand Slam
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
            "Unknown Tournament"
        )



        if not is_top_atp_tournament(tournament):

            continue




        home = event.get(
            "home",
            "Unknown"
        )


        away = event.get(
            "away",
            "Unknown"
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
            event.get(
                "odds",
                {}
            ),



            "h2h":
            "unknown"

        }



        matches.append(match)




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
