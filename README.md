# FAME – Food AI Meal Engine

*Autore: Mirko Calcaterra*

---

## Introduzione

**FAME** ( **F**ood **A**I **M**eal **E**ngine) è una web‑app intelligente pensata per trasformare le linee guida nutrizionali di un dietista in:

1. un **piano alimentare settimanale** personalizzato (colazione, pranzo, merenda, cena – configurabili),
2. la **lista della spesa** ottimizzata per quantità, stagionalità e numero di persone in casa,
3. schede pasto con ricetta, valori nutrizionali e **video‑tutorial YouTube**.

L’app è **mobile‑first**, gira in un singolo container **Python + FastAPI** (backend) e **React (TypeScript)** (frontend) e sfrutta **Google Gemini LLM** per generare menu bilanciati. Il progetto può essere distribuito sia su **Render** sia su **Replit Deployments**.

---

## Funzionalità Principali

| Modulo                | Descrizione                                                                                                                                                                                                                                      |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Autenticazione**    | Login/Register con email + password, JWT stateless, recupero password.                                                                                                                                                                           |
| **Onboarding**        | Questionario multi‑step al primo accesso: sesso, età, peso, altezza, sport praticato, allergie/intolleranze, membri della famiglia, obiettivo (mettere massa / dimagrire), pasti da includere. Tutti i dati sono modificabili in *Impostazioni*. |
| **Home → Calendario** | Vista settimanale (drag & drop) dei pasti generati. **FAB** in basso a destra con:<br>1. *Carica dieta* (PDF/immagine → OCR)<br>2. *Prenota consulto* (link esterno NutriDoc)<br>3. *Genera piano*                                               |
| **Generazione piano** | Chiamata a Google Gemini con prompt parametrico ⟶ ritorno JSON descrittivo ➜ salvataggio su DB ➜ rendering sul calendario. L’algoritmo filtra ingredienti **di stagione** (calendario UE) e rispetta allergie, obiettivi calorici e macro.       |
| **Scheda Pasto**      | Titolo, descrizione, ingredienti (grammatura scalata), istruzioni passo‑passo, link YouTube alla ricetta, valori nutrizionali.                                                                                                                   |
| **Lista della Spesa** | Aggregazione automatica ingredienti per la settimana, raggruppati per reparto supermercato, scaricabile in PDF/CSV.                                                                                                                              |
| **Impostazioni**      | Profilo utente, preferenze alimentari, numero persone in casa, target peso/massa.                                                                                                                                                                |

---

## Obiettivi Didattici

In \~4 ore di laboratorio gli studenti impareranno a:

* **Collaborare in team** (4 persone) con GitHub/Replit e metodologie *AI‑assisted* ("vibe coding").
* **Progettare un flusso utente completo**: auth → onboarding → dashboard → generatori AI → export.
* Integrare **Google Gemini**, **YouTube Data API** (e facoltativamente Spoonacular) in un backend FastAPI.
* Creare un frontend React mobile‑first con **React Big Calendar**, **Tailwind** e **shadcn/ui**.
* Scrivere prompt efficaci per LLM e gestire la post‑elaborazione JSON.
* Effettuare test end‑to‑end e deploy su Render/Replit.

Alla fine il team consegnerà una web‑app production‑ready che produce menu settimanali personalizzati con shopping list e video ricette.

---

## Prerequisiti

* **Account Replit** **oppure** macchina locale con Node ≥20 e Python ≥3.10
* **GitHub** (repo privato consigliato)
* **Google Cloud Platform**: abilita

  * *Generative AI API* (Gemini) → `GEMINI_API_KEY`
  * *YouTube Data API v3* → `YOUTUBE_API_KEY`
* (Opz.) **Spoonacular API** → `SPOONACULAR_KEY`
* Librerie Python: `fastapi`, `uvicorn`, `sqlalchemy`, `python-jose[cryptography]`, `google-generative-ai`, `google-api-python-client`, `python-dotenv`.
* Tool CLI: `git`, `docker` (facoltativo), `render-cli` (se deploy su Render).

---

## Divisione Ruoli (suggerita)

1. **Frontend Developer** – UI/UX, React Big Calendar, Tailwind.
2. **Backend Developer** – FastAPI, DB models, JWT, integrations.
3. **Prompt Engineer / AI Specialist** – prompt Gemini, post‑processing, stagionalità.
4. **DevOps & QA** – CI/CD (GitHub Actions), secrets, deploy, test e2e.

> ★ Suggerimento: i primi prompt al modello scriveteli insieme per allinearvi su formato output e requisiti.

---

## Metodologia "Vibe Coding"

1. **Descrivi** ad alta voce/la chat la funzionalità desiderata.
2. **Genera** codice con AI (Lovable, Ghostwriter, Cursor…).
3. **Valida & refina**: leggi il codice, testalo, correggi. Repeat.

Questo ciclo rapido permette di mantenere il focus sul *cosa* più che sul *come*, accelerando lo sviluppo senza perdere qualità.

---

## Timeline Suggerita (4 Ore)

### Sessione 1 (0:00 ‑ 0:20) – Kick‑off & Setup

* Crea repo GitHub ➜ importa in Replit (template Nix).
* Struttura cartelle `backend/`, `frontend/`.
* Aggiungi `.env.example` con chiavi richieste.
* Endpoint FastAPI "Hello World" per verifica:

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"msg": "FAME backend up"}
```

### Sessione 2 (0:20 ‑ 1:30) – UI prototipo & skeleton API

* **Frontend**: prompt Lovable → Login/Register page, Onboarding Stepper, Calendar view.
* **Backend**: modelli Pydantic `User`, `Profile`, `MealPlanRequest`.
* Rotta protetta `POST /mealplan` (placeholder response).
* Abilita CORS + JWT middleware.

### Sessione 3 (1:30 ‑ 2:45) – AI Integration & Business Logic

* Scrivi prompt Gemini con segnaposto ({{calorie}}, {{allergie}}, …).
* Implementa funzione `generate_mealplan()` che:

  1. invoca Gemini,
  2. filtra ingredienti di stagione,
  3. persiste su DB.
* Aggiungi ricerca YouTube per ciascuna ricetta:

```python
from googleapiclient.discovery import build

def youtube_search(query: str) -> str:
    yt = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    res = yt.search().list(q=query, part="id", maxResults=1, type="video").execute()
    return f"https://youtu.be/{res['items'][0]['id']['videoId']}"
```

### Sessione 4 (2:45 ‑ 4:00) – Feature Completing, Testing & Deploy

* Completa *Lista della Spesa* endpoint `GET /shopping-list` (aggregazione + scaling porzioni).
* Test UI end‑to‑end su mobile emulator.
* Configura `render.yaml` **oppure** `.replit` + `replit.nix`, aggiungi secrets.
* Deploy ➜ demo live.

---

## Comandi Rapidi

```bash
# Avvio locale
uvicorn backend.main:app --reload & npm --prefix frontend run dev

# Build SPA dentro FastAPI (prod)
npm --prefix frontend run build
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

---

## Conclusioni

Con FAME porterai l’IA generativa in cucina, offrendo piani alimentari personalizzati, stagionali e facili da seguire – il tutto in poche ore di sviluppo collaborativo 😊.
