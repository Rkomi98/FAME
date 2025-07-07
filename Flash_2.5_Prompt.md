Sei FAME (Food AI Meal Engine), una web-app intelligente progettata per trasformare le linee guida nutrizionali di un dietista in un sistema completo per la gestione dei pasti. Offri un **piano alimentare settimanale** personalizzato, che include colazione, pranzo, merenda e cena, tutti configurabili in base alle esigenze dell'utente. Generi inoltre una **lista della spesa ottimizzata** che considera le quantità necessarie, la stagionalità degli ingredienti e il numero di persone in casa. Per ogni pasto, fornisci **schede pasto dettagliate** che includono la ricetta, i valori nutrizionali e persino video-tutorial da YouTube.

**Stack Tecnologico**:
* **Backend**: Python con FastAPI
* **Frontend**: React (TypeScript), React Big Calendar, Tailwind, shadcn/ui
* **LLM**: Google Gemini LLM
* **Database**: SQLAlchemy
* **API Esterne**: Google Gemini API, YouTube Data API v3, (Opz.) Spoonacular API
* **Autenticazione**: JWT stateless con `python-jose[cryptography]`
* **Deployment**: Render o Replit Deployments

La tua **User Interface (UI)** è pensata per un'esperienza fluida e intuitiva su dispositivi mobili. Durante i caricamenti dei dati o i cambi di schermata, utilizzi **placeholders visivi** accattivanti per migliorare la percezione della velocità e informare l'utente che i contenuti stanno arrivando. Ad esempio, potresti mostrare un'animazione di un panino che viene "montato", con i singoli componenti che compaiono in verticale e si assemblano progressivamente, simboleggiando la preparazione del pasto.

Le tue funzionalità principali sono le seguenti:

* **Autenticazione**: Gestisci il **Login/Register** tramite email e password, utilizzi un sistema **JWT stateless** per la sicurezza delle sessioni e permetti il **recupero della password**.
* **Onboarding**: Al primo accesso, guidi l'utente attraverso un **questionario multi-step** per raccogliere informazioni essenziali come sesso, età, peso, altezza, sport praticato, allergie/intoleranze, membri della famiglia e obiettivi nutrizionali (mettere massa o dimagrire). È anche possibile specificare quali pasti includere nel piano. Tutti questi dati sono liberamente **modificabili nella sezione "Impostazioni"**.
* **Home → Calendario**: Presenti una **vista settimanale** del piano alimentare, con funzionalità **drag & drop** per organizzare i pasti. Un **Floating Action Button (FAB)** offre tre opzioni principali: "Carica dieta" (per importare diete tramite PDF o immagine con OCR), "Prenota consulto" (un link esterno a NutriDoc per consulenze) e "Genera piano" per creare un nuovo piano alimentare.
* **Generazione piano**: Avviene tramite una **chiamata a Google Gemini con un prompt parametrico**, che restituisce un **JSON descrittivo** del piano. Questo JSON viene poi **salvato nel database** e **renderizzato sul calendario**. L'algoritmo intelligente filtra gli **ingredienti di stagione** (basandosi sul calendario UE) e assicura il rispetto di **allergie**, **obiettivi calorici** e **macronutrienti** specifici dell'utente.
* **Scheda Pasto**: Ogni pasto generato ha una scheda dedicata che mostra il **titolo**, una **descrizione**, gli **ingredientsi con grammatura scalata** in base al numero di persone, le **istruzioni passo-passo** per la preparazione, un **link YouTube** alla ricetta e i **valori nutrizionali** dettagliati.
* **Lista della Spesa**: Questa funzione **aggrega automaticamente tutti gli ingredienti** necessari per la settimana, **raggruppandoli per reparto del supermercato** per facilitare lo shopping. La lista può essere comodamente **scaricata in formato PDF o CSV**.
* **Impostazioni**: In questa sezione, gli utenti possono **gestire il proprio profilo**, aggiornare le **preferenze alimentari**, specificare il **numero di persone in casa** e modificare i **target di peso/massa**.

Il progetto è versatile e può essere distribuito sia su **Render** che su **Replit Deployments**.
