import requests
from datetime import datetime

TELEGRAM_TOKEN = "8273677003:AAEpTPeJQJed3lFQzTB8o7a_m8ZouNSeIag"
CHAT_ID = "395542510"
ODDS_API_KEY = "8955bc07bfd1e8f4e010287404983814"

def send_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, json=payload)

def get_mlb_games():
    url = "https://api.the-odds-api.com/v4/sports/baseball_mlb/odds"

    params = {
        "apiKey": ODDS_API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }

    response = requests.get(url, params=params)

    return response.json()

def analyze_games(games):
    picks = []

    for game in games[:3]:
        home = game["home_team"]
        away = game["away_team"]

        bookmakers = game.get("bookmakers", [])

        if not bookmakers:
            continue

        markets = bookmakers[0].get("markets", [])

        for market in markets:
            if market["key"] == "h2h":

                outcomes = market["outcomes"]

                favorite = min(outcomes, key=lambda x: x["price"])

                picks.append(
                    f"⚾ {favorite['name']} ML vs {away if favorite['name']==home else home} @ {favorite['price']}"
                )

    return picks

def run():
    games = get_mlb_games()

    picks = analyze_games(games)

    if not picks:
        send_message("📉 Hoy no encontré apuestas con valor suficiente.")
        return

    message = "🔥 PICKS DEL DÍA 🔥\n\n"

    for pick in picks:
        message += f"{pick}\n"

    message += f"\n📅 {datetime.now().strftime('%d/%m/%Y')}"

    send_message(message)

run()
