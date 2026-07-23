from datetime import datetime


ALLOWED_TOURNAMENTS = [
    "ATP 500",
    "ATP Masters 1000",
    "Grand Slam"
]


def get_atp_matches():

    today = datetime.now().strftime("%Y-%m-%d")


    # ČIA VĖLIAU BUS REALUS API
    # Dabar testuojame filtravimo logiką

    all_matches = [

        {
            "date": today,
            "tournament": "ATP Masters 1000",
            "surface": "Hard",
            "player1": "Player A",
            "player2": "Player B",
            "ranking1": 3,
            "ranking2": 8
        },


        {
            "date": today,
            "tournament": "ATP 250",
            "surface": "Clay",
            "player1": "Player C",
            "player2": "Player D",
            "ranking1": 40,
            "ranking2": 55
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
