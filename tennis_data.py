from datetime import datetime


ALLOWED_TOURNAMENTS = [
    "ATP 500",
    "ATP Masters 1000",
    "Grand Slam"
]



def get_atp_matches():

    today = datetime.now().strftime("%Y-%m-%d")


    # TESTINIAI DUOMENYS
    # Vėliau čia jungsim realų šaltinį

    all_matches = [

        {
            "date": today,

            "tournament": "ATP Masters 1000",

            "surface": "Hard",


            "player1": {

                "name": "Jannik Sinner",

                "ranking": 1,

                "form": "8/10",

                "serve_rating": 9,

                "return_rating": 9
            },


            "player2": {

                "name": "Daniil Medvedev",

                "ranking": 6,

                "form": "6/10",

                "serve_rating": 8,

                "return_rating": 8
            },


            "h2h": "Sinner leads 6-5",


            "odds": {

                "player1": 1.55,

                "player2": 2.60
            }

        },


        {

            "date": today,

            "tournament": "ATP 500",

            "surface": "Clay",


            "player1": {

                "name": "Carlos Alcaraz",

                "ranking": 2,

                "form": "9/10",

                "serve_rating": 9,

                "return_rating": 9
            },


            "player2": {

                "name": "Casper Ruud",

                "ranking": 8,

                "form": "7/10",

                "serve_rating": 8,

                "return_rating": 8
            },


            "h2h": "Alcaraz leads 4-1",


            "odds": {

                "player1": 1.40,

                "player2": 3.00
            }

        }

    ]



    filtered = []


    for match in all_matches:

        if match["tournament"] in ALLOWED_TOURNAMENTS:

            filtered.append(match)



    if len(filtered) == 0:

        return {

            "status": "empty",

            "message":
            "🎾 Šiandien nėra tinkamų ATP TOP lygio mačų"

        }



    return {

        "status": "ok",

        "matches": filtered

    }
