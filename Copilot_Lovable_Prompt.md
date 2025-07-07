# Prompt Lovable – FAME: Food AI Meal Engine – Frontend React

## Obiettivo

Sviluppare l’interfaccia utente mobile‑first dell’applicazione **FAME – Food AI Meal Engine**, una web‑app che genera piani alimentari settimanali personalizzati a partire da linee guida dietetiche. Il backend è basato su **FastAPI** e si integra con **Google Gemini** per la generazione dei menu. L’app include promemoria idratativi e supporta vincoli di frequenza sportiva e budget alimentare impostati dall’utente durante l’onboarding.

---

## Stack Tecnologico

### Frontend

- **React** con **TypeScript**
- **TailwindCSS** per lo styling
- **shadcn/ui** per i componenti predefiniti
- **React Big Calendar** per la visualizzazione del piano settimanale
- **React Router** per la navigazione
- **React Query** (opzionale)
- **LocalStorage** per memorizzazione del JWT
- **fetch API** per la comunicazione con il backend

### Backend

- **FastAPI** (Python ≥3.10)
- **Uvicorn** come server ASGI
- **SQLAlchemy** per gestione ORM
- **Google Generative AI SDK** per interazione con Gemini
- **Google API Python Client** per YouTube Data API
- **python-jose[cryptography]** per JWT
- **python-dotenv** per configurazioni ambiente
- **OCR (facoltativo)** per estrazione testi da PDF/immagini
- **Render** o **Replit Deployments** per pubblicazione live

---

## Pagine & Componenti da Implementare

### 1. `AuthPage.tsx` – Autenticazione
- Form login/registrazione con email + password
- Toggle login/signup
- Validazione form con messaggi di errore
- Link “Password dimenticata”
- Salvataggio JWT in `localStorage`

---

### 2. `OnboardingStepper.tsx` – Onboarding multi-step
- Raccolta dati utente tramite form a step:
  - sesso, età, peso, altezza
  - sport praticato:
    - tipo di sport
    - **frequenza settimanale (es. 3 volte a settimana)**
  - allergie / intolleranze alimentari
  - obiettivo nutrizionale: dimagrire / mettere massa
  - pasti da includere: colazione, pranzo, merenda, cena
  - membri della famiglia
  - **budget alimentare mensile indicativo** (usato per filtrare ingredienti e ricette)
  - **promemoria acqua**: se abilitato, specificare ogni quante ore ricevere un alert
- Stato gestito localmente con barra di avanzamento
- Invio dati al backend al termine

---

### 3. `CalendarView.tsx` – Calendario pasti
- Vista settimanale con drag&drop dei pasti generati
- `React Big Calendar` customizzato
- Floating Action Button (FAB):
  1. Carica dieta (placeholder OCR PDF/immagine)
  2. Prenota consulto (link NutriDoc)
  3. Genera piano (chiamata backend → Gemini)

---

### 4. `MealCard.tsx` – Scheda pasto
- Titolo e descrizione
- Ingredienti con grammatura scalata
- Istruzioni step-by-step
- Link YouTube video ricetta
- Valori nutrizionali: calorie, macro

---

### 5. `ShoppingListPage.tsx` – Lista della spesa
- Aggregazione ingredienti per i pasti della settimana
- Raggruppamento per reparto (ortofrutta, latticini…)
- Download PDF/CSV
- UI leggibile e stampabile

---

### 6. `SettingsPage.tsx` – Impostazioni utente
- Modifica dati personali e preferenze
- Obiettivo nutrizionale e numero persone in casa
- Allergie / pasti preferiti
- **Gestione promemoria acqua**: attiva/disattiva, intervallo orario
- **Aggiornamento frequenza sportiva e budget alimentare**

---

## Funzionalità Aggiuntive

- Applicazione genera menu personalizzati in base a:
  - obiettivo calorico e preferenze alimentari
  - ingredienti di stagione
  - vincoli di allergie, sport praticato e budget
- Reminder automatici per bere acqua secondo intervallo impostato
- Integrazione video YouTube nelle schede pasto
- Lista della spesa ottimizzata per quantità e numero di persone

---

## Struttura Consigliata

- `frontend/pages/`: pagine principali
- `frontend/components/`: componenti riutilizzabili
- `frontend/hooks/`: custom hooks (fetch, reminder acqua, onboarding state)
- `frontend/utils/`: utility varie (formatter, validazioni form)

---

## Specifiche

- Chiamate API asincrone con gestione errori
- Componenti modulari e tipizzati con commenti esplicativi
- Layout responsivo per smartphone, tablet e desktop
- Navigazione gestita con `React Router`
- Esperienza utente fluida, accessibile, coerente
