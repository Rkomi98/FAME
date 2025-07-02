# **FAME 2.0 – The Bio-Integrated Meal Engine**

*Autore Originale: Mirko Calcaterra*
*Estensione Proposta: Gemini AI Assistant*

---

## Introduzione

**FAME 2.0** è l'evoluzione del **F**ood **A**I **M**eal **E**ngine. Non è più solo una web-app che traduce le linee guida di un dietista, ma un vero e proprio **assistente nutrizionale dinamico** che si sincronizza con la tua vita.

Il cuore del progetto è l'integrazione con i dati biometrici del tuo smartwatch (es. Apple Watch, Samsung/Galaxy Watch). FAME 2.0 non si limita a generare un piano statico, ma lo **adatta quotidianamente** in base a:
1.  **Calorie bruciate** durante il giorno.
2.  **Qualità del sonno** della notte precedente.
3.  **Livelli di attività fisica** (passi, minuti di allenamento).

Trasformiamo i dati del tuo corpo in un piano alimentare che evolve con te, con tanto di lista della spesa ottimizzata e video-ricette. L'architettura rimane un container **Python + FastAPI** e **React (TypeScript)**, ma con un'intelligenza potenziata.

---

## Funzionalità Principali

| Modulo | Descrizione |
| :--- | :--- |
| **Autenticazione** | Login/Register con email + password, JWT stateless, recupero password. |
| **Onboarding** | Questionario iniziale multi-step: preferenze alimentari, allergie, obiettivi, numero di persone in casa. **Nuovo**: richiesta di autorizzazione per collegare i dati sanitari. |
| **Integrazione Biometrica** | **Collegamento via API a dati sanitari aggregati (es. Google Fit, che centralizza dati da molti wearable).** In alternativa, un **database mock** che simula dati giornalieri di: passi, calorie attive, ore di sonno, frequenza cardiaca a riposo. |
| **Home → Calendario Dinamico** | Vista settimanale del piano alimentare. I pasti passati sono fissi, quelli futuri possono essere **ri-calcolati automaticamente** a fine giornata in base ai dati biometrici. Un'icona indicherà se il pasto è stato "adattato". |
| **Generazione Piano Adattivo** | Chiamata a **Google Gemini** con un prompt arricchito: oltre a preferenze e allergie, include i **dati biometrici della giornata precedente** (es. "L'utente ieri ha bruciato 450kcal extra e dormito solo 5 ore. Adegua l'energia e i micronutrienti per il recupero"). L'algoritmo continua a privilegiare ingredienti di stagione. |
| **Scheda Pasto** | Titolo, descrizione, ingredienti (grammatura scalata), istruzioni, **link YouTube** alla ricetta, valori nutrizionali dettagliati. |
| **Lista della Spesa** | Aggregazione degli ingredienti per la settimana. **Nuovo**: possibilità di "congelare" il piano per generare una lista definitiva o di riceverne una "stimata" con possibili variazioni. |
| **Impostazioni** | Gestione profilo, preferenze, membri della famiglia e **gestione delle connessioni API** (es. "Scollega Google Fit"). |

---

## Obiettivi Didattici (Hackathon ~8 Ore / 2 Giorni)

Gli studenti impareranno a:
*   **Collaborare** in un ambiente "vibe coding" usando strumenti AI-assisted.
*   Progettare un sistema che **risponde a input dinamici** del mondo reale (dati biometrici).
*   **Integrare API di terze parti con autenticazione OAuth 2.0** (Google Fit) o, in alternativa, a creare e usare un **mock data provider** realistico.
*   Scrivere **prompt per LLM significativamente più complessi e contestuali**.
*   Gestire la logica di un'applicazione che si "auto-corregge" (i piani alimentari adattivi).
*   Sviluppare un backend FastAPI robusto e un frontend React reattivo e mobile-first.

---

## Prerequisiti

*   **Account Replit/GitHub** e macchina locale (Node ≥20, Python ≥3.10).
*   **Google Cloud Platform**:
    *   *Generative AI API* (Gemini) → `GEMINI_API_KEY`
    *   *YouTube Data API v3* → `YOUTUBE_API_KEY`
    *   **(Nuovo/Consigliato)** *Google Fit API* → Abilita l'API e crea credenziali OAuth 2.0 (Client ID & Secret).
*   Librerie Python: `fastapi`, `uvicorn`, `sqlalchemy`, `python-jose[cryptography]`, `google-generative-ai`, `google-api-python-client`, **(Nuovo)** `google-auth-oauthlib`.

---

## Divisione Ruoli (Suggerita per 4 Persone)

1.  **Frontend Developer (React & UI/UX)**: Si occupa della UI, del calendario (`React Big Calendar`), dello stepper di onboarding e della visualizzazione dei dati, inclusi quelli biometrici.
2.  **Backend Developer (Core & Auth)**: Sviluppa le API per utenti, pasti, e soprattutto **gestisce il flusso OAuth 2.0 per l'integrazione con Google Fit** e la memorizzazione sicura dei token.
3.  **AI & Data Specialist (Prompt & Logic)**: Progetta il **prompt adattivo** per Gemini. Crea la logica per recuperare i dati biometrici (reali o mock) e per fonderli con le preferenze dell'utente prima di chiamare l'LLM. Sviluppa l'algoritmo di stagionalità.
4.  **Integration & QA Specialist (The Glue)**: Assicura che frontend e backend comunichino correttamente. Sviluppa il **mock data provider** per i dati biometrici, scrive test end-to-end e gestisce il deploy.

> ★ Suggerimento: la definizione della **struttura dati biometrica** (sia essa reale da API o mock) è il primo task da fare tutti insieme.

---

### **Come integrare i dati dello Smartwatch: Opzione A (Realistica) e B (Hackathon-Friendly)**

**A) API Reale (Google Fit):**
Il Backend Developer implementa il flusso OAuth 2.0. Il frontend reindirizza l'utente a una pagina di consenso di Google. Una volta ottenuta l'autorizzazione, il backend riceve un token per interrogare l'API di Google Fit e recuperare dati come `aggregate_by_calories_expended`, `aggregate_by_step_count_delta`, ecc.

**B) Mock Database (Hackathon-Friendly):**
L'Integration Specialist crea un modulo Python, es. `biometric_provider.py`, che simula la risposta di un'API.

```python
# backend/biometric_provider.py
import random
from datetime import datetime, timedelta

def get_biometric_data_for_user(user_id: int, date: datetime) -> dict:
    """Simula i dati biometrici per un utente in una data specifica."""
    # Logica per rendere i dati consistenti per lo stesso utente/giorno
    random.seed(f"{user_id}-{date.strftime('%Y-%m-%d')}")
    
    return {
        "date": date.strftime('%Y-%m-%d'),
        "active_calories_burned": random.randint(250, 800),
        "steps": random.randint(4000, 15000),
        "sleep_hours": round(random.uniform(4.5, 8.5), 1),
        "resting_heart_rate": random.randint(55, 75)
    }
```
Il resto dell'app userà questa funzione come se stesse chiamando una vera API.

---

## Timeline Suggerita (Hackathon 2 Giorni / ~8 Ore)

### **Giorno 1 (4 Ore) – Le Basi di FAME**

*   **(0:00 - 0:30) Kick-off & Setup:**
    *   Setup repo, cartelle `backend/`, `frontend/`, file `.env`.
    *   Definizione condivisa della struttura dati (inclusi i campi biometrici).
*   **(0:30 - 2:00) Auth e UI Scheletro:**
    *   **Backend**: Modelli Pydantic, auth con JWT, rotte protette.
    *   **Frontend**: Pagine Login/Register, Onboarding (senza logica), vista Calendario vuota.
*   **(2:00 - 4:00) Generazione Piano Base & Mock Provider:**
    *   **AI/Data**: Implementa il prompt *base* (non ancora adattivo) e la funzione `generate_mealplan()`.
    *   **Integration/QA**: Sviluppa e testa il `biometric_provider.py` (Opzione B).
    *   **Team**: Integrate il tutto per generare un primo piano alimentare statico e visualizzarlo in calendario.

### **Giorno 2 (4 Ore) – L'Integrazione Bio-Adattiva**

*   **(4:00 - 6:00) Integrazione Dati Biometrici:**
    *   **Backend**: Implementa il flusso OAuth 2.0 (Opzione A) o un endpoint che usi il mock provider (Opzione B).
    *   **AI/Data**: Modifica il prompt per includere i dati biometrici. La funzione `generate_mealplan()` ora deve prima recuperare questi dati.
    *   **Frontend**: Aggiungi il pulsante "Connetti a Google Fit" e visualizza i dati biometrici recuperati sulla dashboard.
*   **(6:00 - 7:30) Logica Adattiva e Feature Finali:**
    *   **Team**: Implementate la logica di ri-calcolo del piano. Ad esempio, un pulsante "Adatta il piano di domani" che rinfresca il piano usando i dati di oggi.
    *   Completate la feature "Lista della Spesa".
*   **(7:30 - 8:00) Testing Finale e Deploy:**
    *   Testate il flusso completo end-to-end.
    *   Configurate `render.yaml` o `.replit` e fate il deploy.
    *   Preparatevi per la demo!

---

## Conclusioni

Con FAME 2.0, non si costruisce solo un generatore di diete, ma un vero partner per il benessere che ascolta il corpo dell'utente. È un progetto che spinge a pensare a sistemi software complessi, dinamici e profondamente personalizzati, offrendo un'esperienza didattica di altissimo livello.
