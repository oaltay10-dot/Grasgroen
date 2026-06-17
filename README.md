# Mijn Gemini-project

Een klein Python-programma dat vragen stelt aan Google Gemini.

## Stap 1 — Pakketten installeren

```powershell
pip install -r requirements.txt
```

## Stap 2 — API-sleutel ophalen

1. Ga naar https://aistudio.google.com/apikey
2. Log in met je Google-account
3. Klik op **Create API key** en kopieer de sleutel

## Stap 3 — Sleutel instellen

1. Kopieer het bestand `.env.example` naar `.env`
2. Zet in `.env` je echte sleutel achter `GEMINI_API_KEY=`

> Deel het `.env`-bestand nooit met anderen — het bevat je geheime sleutel.

## Stap 4 — Programma starten

```powershell
python main.py
```

Stel een vraag en Gemini antwoordt. Typ `stop` om af te sluiten.
