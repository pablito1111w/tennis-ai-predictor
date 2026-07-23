import os
from datetime import datetime

import requests


ODDS_API_KEY = os.environ["ODDS_API_KEY"]


ALLOWED_KEYWORDS = [
    "atp",
    "masters",
    "grand slam",
    "wimbledon",
    "us open",
    "australian open",
    "roland garros",
    "french open"
]


def get_events():

    url = "https://api.odds-api.io/v3/events"

    params = {
        "apiKey": ODDS_API_KEY,
        "sport": "tennis",
        "status": "pending"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, list):
            return data

        return []

    except Exception as e:

        print("Odds API klaida:", str(e))

        return []



def is_top_atp_tournament(league_name):

    league_name = league_name.lower()

    return any(
        keyword in league_name
        for keyword in ALLOWED_KEYWORDS
    )



def get_atp_matches():

    today = datetime.now().strftime("%Y-%m-%d")

    events = get_events()

    matches = []

    for event in events:

        league = event.get("league", {})

        tournament = league.get(
            "name",
            "Unknown Tournament"
        )

        if not is_top_atp_tournament(
            tournament
        ):
            continue

        match = {

            "date": today,

            "event_id":
            event.get("id"),

            "tournament":
            tournament,

            "player1": {
                "name":
                event.get("home", "Unknown"),
                "ranking":
                "unknown",
                "form":
                "unknown"
            },

            "player2": {
                "name":
                event.get("away", "Unknown"),
                "ranking":
                "unknown",
                "form":
                "unknown"
            },

            "odds": {},

            "h2h":
            "unknown"
        }

        matches.append(match)

    if len(matches) == 0:

        return {
            "status": "empty",
            "message":
            "🎾 Šiandien nerasta ATP 500 / ATP Masters 1000 / Grand Slam mačų"
        }

    return {
        "status": "ok",
        "matches": matches
    }
