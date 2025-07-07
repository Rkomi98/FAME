**Prompt completo per Lovable Dev - FAME (Food AI Meal Engine)**

### Descrizione del progetto

FAME (Food AI Meal Engine) è un'applicazione web intelligente che aiuta i dietisti e gli utenti finali nella gestione e ottimizzazione della nutrizione settimanale attraverso:

1. **Generazione automatica di un piano alimentare personalizzato**: pasti configurabili (colazione, pranzo, merenda, cena).
2. **Lista della spesa intelligente** basata su quantità, stagionalità e numero di persone.
3. **Schede pasto dettagliate** con ricette, valori nutrizionali e video-tutorial YouTube.

L'applicazione avrà un design mobile-first basato su:

* Frontend React con TypeScript
* Backend FastAPI (Python)
* Integrazione Google Gemini per la generazione intelligente dei pasti
* YouTube Data API per tutorial video
* Spoonacular API (opzionale) per ulteriori dati nutrizionali

### Stack Tecnologico

* **Frontend**:

  * React (TypeScript)
  * Tailwind CSS
  * React Big Calendar per la gestione calendario
  * shadcn/ui per componenti UI eleganti e funzionali

* **Backend**:

  * FastAPI con Python 3.13
  * Uvicorn per il server ASGI
  * SQLAlchemy ORM per la gestione database
  * JWT stateless authentication (python-jose\[cryptography])
  * Integrazione di Google Gemini con google-generative-ai
  * YouTube Data API (google-api-python-client)
  * Spoonacular API (opzionale)
  * Python-dotenv per gestione variabili ambientali

### Cloud e deployment

* Google Cloud Platform:

  * Generative AI API (Gemini) con GEMINI\_API\_KEY
  * YouTube Data API v3 con YOUTUBE\_API\_KEY
  * (Opz.) Spoonacular API con SPOONACULAR\_KEY

* Deploy:

  * Render o Replit
  * Docker opzionale per containerizzazione
  * Git per version control
  * render-cli per deployment

### Struttura e funzionalità

**Autenticazione**

* Login/Register via email + password
* JWT stateless authentication
* Recupero password via email

**Onboarding (questionario)**

* Informazioni base: sesso, età, peso, altezza, sport praticato
* Allergie/intolleranze, membri famiglia, obiettivi (massa/dimagrimento)
* Scelta pasti preferiti (modificabile in impostazioni)

**Home → Calendario**

* Vista calendario settimanale drag & drop
* FAB con:

  1. Caricamento dieta (PDF/immagine → OCR)
  2. Prenotazione consulto (link esterno NutriDoc)
  3. Generazione automatica piano settimanale

**Generazione Piano**

* Prompt parametrico per Google Gemini:

  * stagionalità ingredienti (EU)
  * allergie/intolleranze
  * calorie/macronutrienti target
* Post-processing efficace del JSON di risposta, salvataggio DB e rendering frontend

**Scheda Pasto**

* Titolo, descrizione dettagliata
* Ingredienti con grammatura scalata
* Istruzioni passo-passo
* Valori nutrizionali dettagliati
* Video YouTube embedded (YouTube Data API)

**Lista della Spesa**

* Aggregazione intelligente ingredienti
* Raggruppamento per reparto supermercato
* Esportazione PDF/CSV

**Impostazioni**

* Profilo utente (dati personali modificabili)
* Preferenze alimentari
* Numero di persone in famiglia
* Target obiettivi peso e massa

### Test e Quality Assurance

* Test end-to-end (E2E) con Cypress o Playwright
* Unit e Integration test backend (pytest)

### Deliverables finali

* Repository GitHub ben strutturato
* Documentazione chiara API con Swagger (FastAPI built-in)
* README dettagliato con istruzioni di installazione, setup e deploy
* Test automatici inclusi nella pipeline CI/CD (Render/Replit)

### Note aggiuntive

* Garantire massima usabilità e intuitività, specialmente per interazioni mobile
* Prompt LLM dettagliati e accurati per minimizzare necessità di correzioni post-processing
* Gestione precisa e sicura delle variabili di ambiente e delle API key