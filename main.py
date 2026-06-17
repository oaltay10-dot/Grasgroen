"""
Mijn Gemini-chatbot met geheugen.

Dit is een algemene chatbot die het hele gesprek onthoudt,
zodat je vervolgvragen kunt stellen (bijv. "en waarom dan?").
"""

import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Lees de geheime sleutel uit het .env-bestand.
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "zet-hier-je-sleutel":
    print("Geen geldige API-sleutel gevonden.")
    print("Maak een bestand '.env' en zet daarin: GEMINI_API_KEY=jouw-sleutel")
    print("Een gratis sleutel haal je op via: https://aistudio.google.com/apikey")
    raise SystemExit(1)

# Maak verbinding met Gemini.
client = genai.Client(api_key=api_key)

# Zo gedraagt de bot zich. Pas deze tekst gerust aan naar jouw smaak!
PERSOONLIJKHEID = (
    "Je bent een vriendelijke, behulpzame assistent die antwoordt in het "
    "Nederlands. Houd je antwoorden helder en niet te lang, tenzij om meer "
    "detail wordt gevraagd."
)

# Maak een chat aan. Deze onthoudt automatisch het hele gesprek.
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(system_instruction=PERSOONLIJKHEID),
)


def main() -> None:
    print("Hoi! Ik ben je Gemini-bot met geheugen. 🤖")
    print("Stel een vraag. Typ 'stop' om te stoppen, of 'reset' om opnieuw te beginnen.\n")

    global chat
    while True:
        vraag = input("Jij: ").strip()

        if vraag.lower() in ("stop", "exit", "quit"):
            print("Tot ziens! 👋")
            break

        if vraag.lower() == "reset":
            chat = client.chats.create(
                model="gemini-2.5-flash",
                config=types.GenerateContentConfig(system_instruction=PERSOONLIJKHEID),
            )
            print("(Geheugen gewist — we beginnen opnieuw.)\n")
            continue

        if not vraag:
            continue

        antwoord = chat.send_message(vraag)
        print("Gemini:", antwoord.text, "\n")


if __name__ == "__main__":
    main()
