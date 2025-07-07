# Prompt Lovable – FAME: Food AI Meal Engine – Frontend React

## Obiettivo

Sviluppare l’interfaccia utente mobile‑first dell’applicazione **FAME – Food AI Meal Engine**, una web‑app che genera piani alimentari settimanali personalizzati a partire da linee guida dietetiche. L’app si integra con un backend **FastAPI** e sfrutta **Google Gemini** per la generazione dei menu. Il frontend deve essere implementato in **React + TypeScript**, con **TailwindCSS** per lo stile e componenti da **shadcn/ui**.

---

## Tecnologie Richieste

- React (TypeScript)
- TailwindCSS
- shadcn/ui
- React Router
- React Big Calendar
- JWT (token in `localStorage`)
- fetch API per comunicare con il backend
- Opzionale: React Query, mobile emulator per test

---

## Pagine & Componenti da Implementare

### 1. `AuthPage.tsx` – Autenticazione
- Form per login e registrazione con email + password
- Toggle tra modalità Login / Signup
- Validazione campi e gestione errori
- Link “Password dimenticata”
- Salvataggio token JWT in `localStorage`
- Layout responsivo, stile wellness moderno

### 2. `OnboardingStepper.tsx` – Onboarding multi‑step
- Raccolta dati utente tramite form guidato:
  - sesso, età, peso, altezza
  - sport praticato
  - allergie / intolleranze
  - obiettivo nutrizionale: dimagrire o mettere massa
  - pasti da includere: colazione, pranzo, merenda, cena
  - membri della famiglia
- Barra di progresso
- Stato persistente e chiamata API finale al backend

### 3. `CalendarView.tsx` – Calendario pasti
- Vista settimanale drag&drop dei pasti
- Uso di `React Big Calendar` customizzato con Tailwind
- Floating Action Button (FAB) con 3 azioni:
  1. Carica dieta (OCR da PDF / immagine – placeholder)
  2. Prenota consulto esterno (link NutriDoc)
  3. Genera piano (trigger backend)

### 4. `MealCard.tsx` – Scheda pasto
- Titolo, descrizione sintetica
- Ingredienti con grammatura (scalata in base al numero persone)
- Istruzioni passo‑passo
- Video tutorial YouTube
- Valori nutrizionali: calorie, macronutrienti

### 5. `ShoppingListPage.tsx` – Lista della spesa
- Aggregazione ingredienti settimanali per pasti generati
- Raggruppamento per reparto supermercato
- Download lista in PDF o CSV
- Visualizzazione mobile-friendly e stampabile

### 6. `SettingsPage.tsx` – Impostazioni utente
- Modifica profilo e preferenze
- Obiettivo peso / massa
- Numero membri in casa
- Gestione pasti inclusi e allergie

---

## Struttura Consigliata

- `frontend/pages/`: pagine principali
- `frontend/components/`: componenti riutilizzabili
- `frontend/hooks/`: custom hooks condivisi
- `frontend/utils/`: funzioni ausiliarie (es. fetch, formatter)

---

## Altre Specifiche

- Tutte le chiamate API sono asincrone con gestione errori
- Componenti modulari e tipizzati
- Commenti esplicativi nel codice
- Navigazione gestita con `React Router`
- Design accessibile, leggibile e coerente (colori pastello, spaziatura ampia)
- Interfaccia testabile via emulatori mobile

---

## Linea guida visiva

- Stile moderno, light e coerente con il settore wellness
- Uso ponderato dei componenti shadcn/ui per form, input, dialog, badge
- Esperienza utente guidata, senza frizioni
