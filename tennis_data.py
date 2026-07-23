def get_atp_matches():

    today = datetime.now().strftime("%Y-%m-%d")

    events = get_events()

    print("\n===== TENNIS EVENTS =====")

    for event in events:

        league = event.get("league", {})

        tournament = league.get(
            "name",
            "Unknown Tournament"
        )

        print("TOURNAMENT:", tournament)

    print("===== END EVENTS =====\n")

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
