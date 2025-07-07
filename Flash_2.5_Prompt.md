Genera un'applicazione web intelligente, **FAME** (Food AI Meal Engine), progettata per trasformare le linee guida nutrizionali di un dietista in un sistema completo per la gestione dei pasti. L'app offre un **piano alimentare settimanale** personalizzato, che include colazione, pranzo, merenda e cena, tutti configurabili in base alle esigenze dell'utente. Genera inoltre una **lista della spesa ottimizzata** che considera le quantità necessarie, la stagionalità degli ingredienti e il numero di persone in casa. Per ogni pasto, fornisce **schede pasto dettagliate** che includono la ricetta, i valori nutrizionali e persino video-tutorial da YouTube.

L'applicazione avrà un design **mobile-first** e sarà basata su un **Frontend React con TypeScript**, un **Backend FastAPI (Python)**, un'integrazione avanzata con **Google Gemini** per la generazione intelligente dei pasti, la **YouTube Data API** per i tutorial video e la **Spoonacular API** (opzionale) per dati nutrizionali aggiuntivi.

La sua **User Interface (UI)** è pensata per un'esperienza fluida e intuitiva su dispositivi mobili. Durante i caricamenti dei dati o i cambi di schermata, l'app utilizzerà **placeholders visivi** accattivanti per migliorare la percezione della velocità e informare l'utente che i contenuti stanno arrivando. Ad esempio, potrebbe mostrare un'animazione di un panino che viene "montato", con i singoli componenti che compaiono in verticale e si assemblano progressivamente, simboleggiando la preparazione del pasto.

---

### **Stack Tecnologico**

* **Backend**:
    * FastAPI con **Python 3.13**
    * **Uvicorn** per il server ASGI
    * SQLAlchemy ORM per la gestione del database
    * JWT stateless authentication (`python-jose[cryptography]`)
    * Integrazione di Google Gemini con `google-generative-ai`
    * YouTube Data API (`google-api-python-client`)
    * Spoonacular API (opzionale)
    * **Python-dotenv** per la gestione delle variabili ambientali
* **Frontend**:
    * React (TypeScript)
    * Tailwind CSS
    * React Big Calendar per la gestione del calendario
    * shadcn/ui per componenti UI eleganti e funzionali

---

### **Cloud e Deployment**

* **Google Cloud Platform**:
    * **Generative AI API (Gemini)** con `GEMINI_API_KEY`
    * **YouTube Data API v3** con `YOUTUBE_API_KEY`
    * (Opz.) **Spoonacular API** con `SPOONACULAR_KEY`
* **Deploy**:
    * Render o Replit
    * **Docker** (opzionale) per containerizzazione
    * **Git** per version control
    * **`render-cli`** per deployment

---

### **Struttura e Funzionalità**

* **Autenticazione**:
    * Login/Register via email + password
    * JWT stateless authentication
    * Recupero password via email

* **Onboarding (Questionario Iniziale)**:
    * Raccolta informazioni base: sesso, età, peso, altezza, sport praticato, **frequenza sport**.
    * Dettagli su allergie/intolleranze, membri della famiglia, obiettivi specifici (massa/dimagrimento).
    * Scelta dei pasti preferiti (modificabile successivamente nelle impostazioni).
    * Definizione di diete particolari (es. vegetariano, vegano, ecc.).
    * Indicazione dello **stato di gravidanza o allattamento (booleano)**.
    * Definizione del **budget per la spesa (basso, medio, alto)**.

* **Home → Calendario**:
    * Presentazione di una vista calendario settimanale con funzionalità drag & drop per l'organizzazione dei pasti.
    * Un Floating Action Button (FAB) con tre opzioni principali:
        1.  **Caricamento dieta**: Importazione di diete da PDF o immagine tramite tecnologia OCR.
        2.  **Prenotazione consulto**: Link esterno a NutriDoc per consulenze professionali.
        3.  **Generazione automatica piano settimanale**.

* **Generazione Piano**:
    * Invio di un prompt parametrico a Google Gemini, includendo:
        * Stagionalità degli ingredienti (basata sul calendario UE).
        * Restrizioni dovute ad allergie/intoleranze.
        * Obiettivi di calorie e macronutrienti target.
    * **Post-processing efficace del JSON di risposta**, salvataggio nel database e **rendering fluido** sul frontend.

* **Scheda Pasto**:
    * Visualizzazione di titolo e descrizione **dettagliata** della ricetta.
    * Elenco degli ingredienti con grammatura scalata in base al numero di persone.
    * Istruzioni passo-passo per la preparazione.
    * Valori nutrizionali dettagliati.
    * Video YouTube embedded (tramite YouTube Data API).

* **Lista della Spesa**:
    * Aggregazione intelligente di tutti gli ingredienti necessari per la settimana.
    * Raggruppamento automatico degli articoli per reparto del supermercato.
    * Funzionalità di esportazione in formato PDF o CSV.

* **Impostazioni**:
    * Gestione del profilo utente (dati personali modificabili).
    * Aggiornamento delle preferenze alimentari.
    * Definizione del numero di persone in famiglia.
    * Modifica degli obiettivi target per peso e massa.

* **Reminder**:
    * Notifiche push ogni due ore per ricordare all'utente di bere acqua.

---

### **Test e Quality Assurance**

* Implementazione di **Test end-to-end (E2E)** con **Cypress o Playwright**.
* Integrazione di **Unit e Integration test** per il backend con **pytest**.

---

### **Deliverables Finali**

* Repository GitHub **ben strutturato**.
* Documentazione chiara delle API con **Swagger (FastAPI built-in)**.
* README **dettagliato** con istruzioni complete di installazione, setup e deploy.
* Inclusione di **test automatici nella pipeline CI/CD (Render/Replit)**.

---

### **Note Aggiuntive**

* Garantire massima usabilità e intuitività dell'interfaccia, specialmente per le interazioni da mobile.
* **Sviluppare prompt LLM dettagliati e accurati per minimizzare la necessità di correzioni post-processing.**
* **Assicurare una gestione precisa e sicura delle variabili di ambiente e delle API key.**
