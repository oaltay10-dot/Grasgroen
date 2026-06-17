"""
Mijn Gemini-chatbot als website.

Start deze website met:
    streamlit run website.py

Er opent dan automatisch een chatpagina in je browser.
"""

import os

import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Zo gedraagt de bot zich. Pas deze tekst gerust aan!
PERSOONLIJKHEID = (
    "Je bent een vriendelijke, behulpzame assistent die antwoordt in het "
    "Nederlands. Houd je antwoorden helder en niet te lang, tenzij om meer "
    "detail wordt gevraagd."
)

# --- Instellingen van de pagina ---
st.set_page_config(page_title="Mijn Gemini-bot", page_icon="🤖")
st.title("🤖 Mijn Gemini-bot")
st.caption("Een chatbot met geheugen, gemaakt met Python en Gemini.")

# --- Verbinding met Gemini (één keer instellen) ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key or api_key == "zet-hier-je-sleutel":
    st.error(
        "Geen geldige API-sleutel gevonden. Zet je sleutel in het bestand '.env' "
        "als GEMINI_API_KEY=jouw-sleutel. Een gratis sleutel: "
        "https://aistudio.google.com/apikey"
    )
    st.stop()


# --- Chat aanmaken en in het geheugen van de website bewaren ---
# st.session_state onthoudt dingen tussen jouw berichten door.
@st.cache_resource
def maak_client():
    return genai.Client(api_key=api_key)


client = maak_client()

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=PERSOONLIJKHEID),
    )
    st.session_state.berichten = []

# --- Knop om opnieuw te beginnen ---
if st.sidebar.button("🔄 Nieuw gesprek"):
    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(system_instruction=PERSOONLIJKHEID),
    )
    st.session_state.berichten = []
    st.rerun()

# --- Toon alle eerdere berichten ---
for bericht in st.session_state.berichten:
    with st.chat_message(bericht["rol"]):
        st.markdown(bericht["tekst"])

# --- Invoerveld onderaan ---
vraag = st.chat_input("Typ hier je bericht...")

if vraag:
    # Toon en bewaar de vraag van de gebruiker.
    st.session_state.berichten.append({"rol": "user", "tekst": vraag})
    with st.chat_message("user"):
        st.markdown(vraag)

    # Vraag het antwoord aan Gemini en toon het.
    with st.chat_message("assistant"):
        with st.spinner("Gemini denkt na..."):
            antwoord = st.session_state.chat.send_message(vraag)
        st.markdown(antwoord.text)

    st.session_state.berichten.append({"rol": "assistant", "tekst": antwoord.text})
