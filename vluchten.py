"""
Vluchten-prijsvergelijker — Nederland naar Zuidoost-Azië.

LET OP: in de modus "Oefenprijzen" zijn de vluchten en prijzen VERZONNEN voorbeelden,
bedoeld om te leren. Kies "Echte prijzen" voor doorklik-knoppen naar echte sites.

Start deze website met:
    streamlit run vluchten.py
"""

import datetime
import random
import urllib.parse

import streamlit as st

# --- Vertrek vanuit Nederland (code -> nette naam) ---
VERTREK_LUCHTHAVENS = {
    "AMS": "Amsterdam (Schiphol)",
    "EIN": "Eindhoven",
    "RTM": "Rotterdam Den Haag",
    "GRQ": "Groningen (Eelde)",
    "MST": "Maastricht Aachen",
}

# --- Bestemmingen in Zuidoost-Azië ---
# duur   = gemiddelde directe vluchtduur in minuten
# tz     = tijdsverschil met Nederland in uren (zomertijd)
# prijs  = realistisch prijsbereik per persoon (enkele reis), in euro
# esim   = Airalo-pagina voor mobiel internet in dat land
BESTEMMINGEN = {
    "BKK": {"naam": "Bangkok", "land": "Thailand", "duur": 660, "tz": 5,
            "prijs": (450, 780), "esim": "https://www.airalo.com/thailand-esim"},
    "DPS": {"naam": "Bali (Denpasar)", "land": "Indonesië", "duur": 900, "tz": 6,
            "prijs": (560, 950), "esim": "https://www.airalo.com/indonesia-esim"},
    "SIN": {"naam": "Singapore", "land": "Singapore", "duur": 780, "tz": 6,
            "prijs": (520, 880), "esim": "https://www.airalo.com/singapore-esim"},
    "KUL": {"naam": "Kuala Lumpur", "land": "Maleisië", "duur": 750, "tz": 6,
            "prijs": (480, 850), "esim": "https://www.airalo.com/malaysia-esim"},
    "SGN": {"naam": "Ho Chi Minh City", "land": "Vietnam", "duur": 730, "tz": 5,
            "prijs": (510, 880), "esim": "https://www.airalo.com/vietnam-esim"},
    "HKT": {"naam": "Phuket", "land": "Thailand", "duur": 800, "tz": 5,
            "prijs": (540, 920), "esim": "https://www.airalo.com/thailand-esim"},
}

# Luchtvaartmaatschappijen voor langeafstandsvluchten (logo + gemiddeld prijsniveau).
MAATSCHAPPIJEN = [
    {"naam": "KLM", "logo": "🔵", "prijsniveau": 1.15},
    {"naam": "Singapore Airlines", "logo": "🟠", "prijsniveau": 1.35},
    {"naam": "Emirates", "logo": "🔴", "prijsniveau": 1.20},
    {"naam": "Qatar Airways", "logo": "🟣", "prijsniveau": 1.25},
    {"naam": "Turkish Airlines", "logo": "🟤", "prijsniveau": 1.05},
    {"naam": "Thai Airways", "logo": "🟪", "prijsniveau": 1.10},
    {"naam": "Lufthansa", "logo": "🟡", "prijsniveau": 1.20},
    {"naam": "Etihad Airways", "logo": "⚪", "prijsniveau": 1.15},
]


def verzin_vluchten(vertrek_code, bestemming_code, info, datum, aantal_passagiers):
    """Maak een lijst met verzonnen vluchten voor de gekozen zoekopdracht.

    We gebruiken een 'seed' op basis van de zoekopdracht, zodat dezelfde zoekopdracht
    steeds dezelfde resultaten geeft (en niet elke seconde verandert).
    """
    seed = hash((vertrek_code, bestemming_code, str(datum)))
    rng = random.Random(seed)

    vluchten = []
    for maatschappij in MAATSCHAPPIJEN:
        for _ in range(rng.randint(1, 2)):
            vertrek_uur = rng.randint(6, 22)
            vertrek_minuut = rng.choice([0, 15, 30, 45])

            # Langeafstand: vaak één overstap, soms direct of twee.
            overstappen = rng.choices([0, 1, 2], weights=[30, 55, 15])[0]
            duur_minuten = info["duur"] + overstappen * rng.randint(120, 360)

            vertrek_tijd = datetime.time(vertrek_uur, vertrek_minuut)
            aankomst_totaal = vertrek_uur * 60 + vertrek_minuut + duur_minuten + info["tz"] * 60
            aankomst_uur = (aankomst_totaal // 60) % 24
            aankomst_tijd = datetime.time(aankomst_uur, aankomst_totaal % 60)

            # Prijs per persoon verzinnen.
            prijs = rng.randint(*info["prijs"]) * maatschappij["prijsniveau"]
            prijs += overstappen * 20
            if datum.weekday() in (4, 5, 6):  # weekend iets duurder
                prijs *= 1.10
            prijs_pp = round(prijs)

            vluchten.append(
                {
                    "maatschappij": maatschappij["naam"],
                    "logo": maatschappij["logo"],
                    "vertrek_tijd": vertrek_tijd,
                    "aankomst_tijd": aankomst_tijd,
                    "duur_minuten": duur_minuten,
                    "overstappen": overstappen,
                    "prijs_pp": prijs_pp,
                    "prijs_totaal": prijs_pp * aantal_passagiers,
                }
            )
    return vluchten


def duur_tekst(minuten):
    """Zet bv. 660 om naar '11u 00m'."""
    return f"{minuten // 60}u {minuten % 60:02d}m"


def toon_aanbevelingen(info):
    """Toon het blok met bestemming-specifieke aanbevelingen (de verdienkant).

    LET OP: dit zijn nog gewone links. Om er geld mee te verdienen meld je je aan bij
    de affiliate-programma's en vervang je de links door jouw persoonlijke affiliate-links.
    """
    naam = info["naam"]
    aanbevelingen = [
        {"emoji": "🎟️", "naam": "Dingen om te doen", "desc": f"Tours & excursies in {naam}",
         "cta": "Bekijk activiteiten →",
         "url": f"https://www.getyourguide.nl/s/?q={urllib.parse.quote(naam)}"},
        {"emoji": "🏨", "naam": "Hotels", "desc": f"Overnachtingen in {naam}",
         "cta": "Vind een hotel →",
         "url": f"https://www.booking.com/searchresults.nl.html?ss={urllib.parse.quote(naam)}"},
        {"emoji": "📱", "naam": "Internet (eSIM)", "desc": f"Mobiel internet voor {info['land']}",
         "cta": "Bekijk eSIM's →", "url": info["esim"]},
        {"emoji": "🧳", "naam": "Reisspullen", "desc": "Handig voor je reis door Azië",
         "cta": "Bekijk op Amazon →",
         "url": "https://www.amazon.nl/s?k=" + urllib.parse.quote("backpack reizen Azië")},
    ]

    kaarten = ""
    for item in aanbevelingen:
        kaarten += f"""
        <a class="rec-card" href="{item['url']}" target="_blank" rel="noopener">
          <div class="rec-emoji">{item['emoji']}</div>
          <div class="rec-name">{item['naam']}</div>
          <div class="rec-desc">{item['desc']}</div>
          <div class="rec-cta">{item['cta']}</div>
        </a>
        """
    st.markdown(
        f"""
        <div class="rec-title">🎒 Handig voor jouw reis naar {naam}</div>
        <div class="rec-sub">Alles om je reis compleet te maken — op één plek.</div>
        <div class="rec-grid">{kaarten}</div>
        """,
        unsafe_allow_html=True,
    )


def vlucht_kaart_html(vlucht, vertrek_code, bestemming_code, is_goedkoopste):
    """Maak de HTML voor één moderne vluchtkaart."""
    if vlucht["overstappen"] == 0:
        stops = '<div class="fc-stops fc-direct">Directe vlucht</div>'
    else:
        woord = "overstap" if vlucht["overstappen"] == 1 else "overstappen"
        stops = f'<div class="fc-stops">{vlucht["overstappen"]} {woord}</div>'

    badge = '<div class="fc-badge">🏆 Goedkoopste</div>' if is_goedkoopste else ""

    return f"""
    <div class="flight-card">
      <div class="fc-airline">
        <span class="fc-logo">{vlucht['logo']}</span>
        <div>
          <div class="fc-name">{vlucht['maatschappij']}</div>
          {stops}
        </div>
      </div>
      <div class="fc-route">
        <div class="fc-time">{vlucht['vertrek_tijd'].strftime('%H:%M')}</div>
        <div class="fc-mid">
          {vertrek_code} &rarr; {bestemming_code}
          <div class="fc-line"></div>
          {duur_tekst(vlucht['duur_minuten'])}
        </div>
        <div class="fc-time">{vlucht['aankomst_tijd'].strftime('%H:%M')}</div>
      </div>
      <div class="fc-price">
        {badge}
        <div class="fc-amount">&euro; {vlucht['prijs_totaal']}</div>
        <div class="fc-pp">&euro; {vlucht['prijs_pp']} p.p.</div>
      </div>
    </div>
    """


def bouw_zoeklinks(vertrek_code, bestemming_code, heen_datum, terug_datum, retour, passagiers):
    """Maak doorklik-links naar Google Flights en Skyscanner, met de reisgegevens al ingevuld."""
    skyscanner = (
        "https://www.skyscanner.nl/transport/vluchten/"
        f"{vertrek_code.lower()}/{bestemming_code.lower()}/"
        f"{heen_datum.strftime('%y%m%d')}/"
    )
    if retour:
        skyscanner += f"{terug_datum.strftime('%y%m%d')}/"
    skyscanner += f"?adults={passagiers}"

    zin = f"Flights from {vertrek_code} to {bestemming_code} on {heen_datum.isoformat()}"
    if retour:
        zin += f" returning {terug_datum.isoformat()}"
    google = "https://www.google.com/travel/flights?q=" + urllib.parse.quote(zin)

    return google, skyscanner


# ----------------- DE WEBSITE -----------------

st.set_page_config(page_title="VluchtVergelijker", page_icon="✈️", layout="centered")

# Strakke, moderne, donkergrijze opmaak.
st.markdown(
    """
    <style>
    .stApp { background-color: #2b2d31; }
    #MainMenu, footer, header { visibility: hidden; }

    /* Eigen kopregel */
    .app-header { padding: 6px 0 18px 0; }
    .app-brand { display: flex; align-items: center; gap: 16px; }
    .app-brand svg { flex-shrink: 0; filter: drop-shadow(0 4px 10px rgba(45,212,191,0.25)); }
    .app-title {
        font-size: 2.1rem; font-weight: 800; letter-spacing: -0.5px;
        background: linear-gradient(90deg, #2dd4bf, #5eead4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .app-sub { color: #9aa0a6; font-size: 1rem; margin-top: 2px; }

    .stButton button, .stLinkButton a, .stFormSubmitButton button {
        border-radius: 10px; font-weight: 600;
    }

    /* --- Moderne vluchtkaart --- */
    .flight-card {
        display: flex; align-items: center; justify-content: space-between;
        background: #363940; border: 1px solid #40444b; border-radius: 16px;
        padding: 16px 22px; margin-bottom: 14px;
        transition: transform .12s ease, border-color .12s ease;
    }
    .flight-card:hover { transform: translateY(-2px); border-color: #2dd4bf; }
    .fc-airline { display: flex; align-items: center; gap: 12px; min-width: 190px; }
    .fc-logo { font-size: 26px; }
    .fc-name { font-weight: 700; font-size: 1.05rem; }
    .fc-stops { font-size: .75rem; color: #9aa0a6; margin-top: 2px; }
    .fc-direct { color: #2dd4bf; }
    .fc-route { display: flex; align-items: center; gap: 16px; flex: 1; justify-content: center; }
    .fc-time { font-size: 1.25rem; font-weight: 700; }
    .fc-mid { text-align: center; color: #9aa0a6; font-size: .78rem; }
    .fc-line {
        height: 2px; width: 90px; background: #5a5f66;
        position: relative; margin: 6px auto;
    }
    .fc-line::after {
        content: '✈'; position: absolute; right: -2px; top: -9px; font-size: .8rem; color: #c5c8cc;
    }
    .fc-price { text-align: right; min-width: 130px; }
    .fc-amount { font-size: 1.5rem; font-weight: 800; color: #2dd4bf; }
    .fc-pp { color: #9aa0a6; font-size: .78rem; }
    .fc-badge {
        display: inline-block; background: #2dd4bf; color: #10231f;
        font-weight: 700; font-size: .68rem; padding: 3px 9px;
        border-radius: 999px; margin-bottom: 6px;
    }

    /* --- Aanbevelingen-blok (affiliate) --- */
    .rec-title { font-size: 1.3rem; font-weight: 800; margin: 26px 0 4px 0; }
    .rec-sub { color: #9aa0a6; font-size: .9rem; margin-bottom: 14px; }
    .rec-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 14px;
    }
    .rec-card {
        display: block; text-decoration: none; color: inherit;
        background: #363940; border: 1px solid #40444b; border-radius: 16px;
        padding: 18px; transition: transform .12s ease, border-color .12s ease;
    }
    .rec-card:hover { transform: translateY(-3px); border-color: #2dd4bf; }
    .rec-emoji { font-size: 30px; }
    .rec-name { font-weight: 700; font-size: 1.02rem; margin-top: 8px; }
    .rec-desc { color: #9aa0a6; font-size: .82rem; margin-top: 3px; }
    .rec-cta { color: #2dd4bf; font-weight: 700; font-size: .82rem; margin-top: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-header">
      <div class="app-brand">
        <svg width="56" height="56" viewBox="0 0 56 56" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0" stop-color="#2dd4bf"/>
              <stop offset="1" stop-color="#5eead4"/>
            </linearGradient>
          </defs>
          <rect x="2" y="2" width="52" height="52" rx="16" fill="url(#g)"/>
          <g transform="translate(13,13) scale(1.25)" fill="#10231f">
            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
          </g>
        </svg>
        <div>
          <div class="app-title">VluchtVergelijker</div>
          <div class="app-sub">Vind de beste vlucht van Nederland naar Zuidoost-Azië</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Het zoekformulier ---
with st.form("zoekformulier"):
    kolom1, kolom2 = st.columns(2)
    with kolom1:
        vertrek_code = st.selectbox(
            "Vertrek vanaf",
            options=list(VERTREK_LUCHTHAVENS.keys()),
            format_func=lambda code: VERTREK_LUCHTHAVENS[code],
        )
    with kolom2:
        bestemming_code = st.selectbox(
            "Bestemming",
            options=list(BESTEMMINGEN.keys()),
            format_func=lambda code: f"{BESTEMMINGEN[code]['naam']} ({code})",
        )

    kolom3, kolom4 = st.columns(2)
    with kolom3:
        heen_datum = st.date_input(
            "Vertrekdatum",
            value=datetime.date.today() + datetime.timedelta(days=30),
            min_value=datetime.date.today(),
        )
    with kolom4:
        passagiers = st.number_input("Aantal passagiers", min_value=1, max_value=9, value=1)

    retour = st.checkbox("Retour (heen én terug)")
    terug_datum = st.date_input(
        "Terugreisdatum",
        value=heen_datum + datetime.timedelta(days=14),
        min_value=heen_datum,
    )

    kolom5, kolom6 = st.columns(2)
    with kolom5:
        alleen_direct = st.checkbox("Alleen directe vluchten")
    with kolom6:
        sorteer_op = st.selectbox(
            "Sorteer op", ["Laagste prijs", "Kortste reisduur", "Vroegste vertrek"]
        )

    prijsbron = st.radio(
        "Prijsbron",
        ["Oefenprijzen (verzonnen)", "Echte prijzen (Google Flights / Skyscanner)"],
        horizontal=True,
    )

    zoeken = st.form_submit_button("🔎 Zoek vluchten", use_container_width=True)


# --- De resultaten tonen ---
if zoeken:
    info = BESTEMMINGEN[bestemming_code]

    if prijsbron.startswith("Echte"):
        google_url, skyscanner_url = bouw_zoeklinks(
            vertrek_code, bestemming_code, heen_datum, terug_datum, retour, passagiers
        )
        reis_tekst = "retour" if retour else "enkele reis"
        st.success(
            f"Klaar! Bekijk echte, actuele prijzen voor {VERTREK_LUCHTHAVENS[vertrek_code]} "
            f"→ {info['naam']} ({reis_tekst}):"
        )
        st.link_button("🔎 Bekijk op Google Flights", google_url, use_container_width=True)
        st.link_button("🔎 Bekijk op Skyscanner", skyscanner_url, use_container_width=True)
        st.caption(
            "De prijzen openen in een nieuw tabblad op de echte vergelijksite, "
            "met jouw reisgegevens al ingevuld."
        )
        toon_aanbevelingen(info)
        st.stop()

    vluchten = verzin_vluchten(vertrek_code, bestemming_code, info, heen_datum, passagiers)
    if alleen_direct:
        vluchten = [v for v in vluchten if v["overstappen"] == 0]

    if sorteer_op == "Laagste prijs":
        vluchten.sort(key=lambda v: v["prijs_totaal"])
    elif sorteer_op == "Kortste reisduur":
        vluchten.sort(key=lambda v: v["duur_minuten"])
    else:  # Vroegste vertrek
        vluchten.sort(key=lambda v: v["vertrek_tijd"])

    if not vluchten:
        st.warning(
            "Geen directe vluchten gevonden naar deze bestemming. "
            "Zet 'Alleen directe vluchten' uit, of probeer Bangkok of Singapore (AMS)."
        )
    else:
        goedkoopste = min(v["prijs_totaal"] for v in vluchten)
        st.success(
            f"{len(vluchten)} vluchten gevonden van {VERTREK_LUCHTHAVENS[vertrek_code]} "
            f"naar {info['naam']}."
        )

        kaarten = "".join(
            vlucht_kaart_html(v, vertrek_code, bestemming_code, v["prijs_totaal"] == goedkoopste)
            for v in vluchten
        )
        st.markdown(kaarten, unsafe_allow_html=True)

        st.info(
            "ℹ️ Let op: dit zijn verzonnen voorbeeldprijzen om te oefenen. "
            "Kies 'Echte prijzen (Google Flights / Skyscanner)' voor live data."
        )
        toon_aanbevelingen(info)
else:
    st.info("Vul hierboven je reisgegevens in en klik op **Zoek vluchten**.")
