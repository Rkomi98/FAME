# Sintesi in un colpo d’occhio

La prima pagina offre Login/Register sicuro con JWT in FastAPI
codingeasypeasy.com
.
Al primo accesso parte un questionario multi-step costruito in React Hook Form/Stepper
claritydev.net
.
Nell’home l’utente vede un calendario drag-&-drop (React Big Calendar) con i pasti generati
dev.to
; in basso a destra può caricare la dieta del nutrizionista o prenotare un consulto via link esterno.
Premendo “Genera piano” il backend invoca Gemini API per produrre ricette settimanali, filtrando per stagionalità (EU produce calendar)
ai.google.dev
agriculture.ec.europa.eu
e usando Spoonacular (o Edamam) per valori nutrizionali/allergeni
spoonacular.com
.
Ogni evento-pasto include ingredienti, dosi, istruzioni e link YouTube ricavato via YouTube Data API v3
developers.google.com
thepythoncode.com
.
La sezione Lista della Spesa raggruppa gli ingredienti, scalati per numero di persone & obiettivo (massa/dimagrimento).
L’intero progetto è deploy-ready su Render con render.yaml e CI GitHub Actions
render.com
.
UI mobile-first con Tailwind responsive utilities
tailwindcss.com
.
Flusso Utente & UX
1. Autenticazione

    Pagina Login / Register (email + password).

    FastAPI + BCrypt hash + JWT Bearer token; refresh opzionale
    codingeasypeasy.com
    .

2. Onboarding (solo al primo login)

    Stepper a più passi (sesso, sport, pasti desiderati, peso, età, altezza, allergie, membri famiglia, obiettivo “massa” / “dimagrire”).

    Salvato in tabella user_profile; modificabile in /settings.

    Implementazione: React Hook Form + custom Stepper
    claritydev.net
    .

3. Home → Calendario

    React Big Calendar per visualizzare e trascinare pasti; localizzato in italiano / GMT+2
    dev.to
    .

    Floating-Action-Button (FAB) con:

        Upload dieta PDF/immagine (OCR lato server).

        Richiedi appuntamento (link a NutriDoc).

        Genera piano settimanale.

4. Generazione Piano

    Endpoint POST /mealplan → chiama Gemini 2.5 con prompt templato. Gemini restituisce 7×N ricette con macro & micro
    ai.google.dev
    .

    Valida stagionalità: confronto con calendario UE produzione
    agriculture.ec.europa.eu
    .

    Completa dati mancanti tramite Spoonacular (allergeni, costi, nutrienti)
    spoonacular.com
    .

5. Event Detail

    Titles, descrizione, ingredienti/dosi in chiaro.

    Link YouTube (primo risultato “Ricetta {titolo}” ordinato per rilevanza) via Data API v3
    developers.google.com
    thepythoncode.com
    .

6. Lista della Spesa

    Endpoint GET /shopping-list?week=YYYY-WW → aggrega ingredienti, scala porzioni per household_size, raggruppa per corsia supermercato.

    Esporti in PDF/CSV o semplice HTML da mobile.

Stack Tecnologico & Integrazioni
Area	Scelte	Note
Frontend	React (TypeScript), Tailwind, shadcn/ui, React Big Calendar, React Query	Mobile-first
tailwindcss.com
Auth	FastAPI, python-jose, BCrypt, JWT Bearer	Stateless
codingeasypeasy.com
AI	Google Gemini SDK	Prompt + parsing JSON
Recipe/Nutri	Spoonacular (allergie, nutrienti)	
spoonacular.com
Video	YouTube Data API v3	
developers.google.com
thepythoncode.com
DB	PostgreSQL (users, profiles, recipes, plans, shopping_list)	
Storage	S3-compatible bucket per file‐upload	
Deploy	Render Web Service + render.yaml; GitHub Actions CI
render.com
	
Infra	Dockerfile multiphase; Uvicorn Gunicorn combo	
Deliverable che Lovable deve produrre

    Albero progetti completo (frontend + backend).

    Pagina Login/Register con JWT flow funzionante.

    Survey onboarding multi-step (React).

    Home con Calendario e FAB azioni.

    Endpoint FastAPI:

        /auth/*, /profile, /diet/upload, /mealplan, /shopping-list.

    Prompt Gemini parametrico + funzione parsing.

    Funzione helper YouTube search (Python) che restituisce videoId.

    Database schema (SQLAlchemy models + migrations).

    render.yaml, Dockerfile, GitHub Action workflow.

    README.md dettagliato con setup + deploy.

