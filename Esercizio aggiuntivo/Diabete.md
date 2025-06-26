---

### **Gluc.IA: Guida all'Hackathon di 2 Giorni**

Questo documento è la vostra mappa per i prossimi due giorni. L'obiettivo non è creare un prodotto perfetto, ma un prototipo funzionante (MVP) che dimostri la potenza delle idee chiave, con un focus sul backend e sull'AI.

#### **Filosofia del Progetto**
*   **Vibe Coding:** Lavorate insieme, nello stesso ambiente (Cursor è perfetto per questo). Parlate costantemente, condividete lo schermo, risolvete i problemi in tempo reale.
*   **Velocità > Perfezione:** È un hackathon. L'obiettivo è avere qualcosa che funzioni per la demo. Un codice "abbastanza buono" che funziona è meglio di un codice perfetto ma incompleto.
*   **Integrazione > Invenzione:** Non reinventate la ruota. Sfruttate API esterne e modelli pre-allenati. Il vostro valore è nel modo in cui *unite* queste tecnologie per risolvere un problema reale.
*   **LLM come trampolino di lancio:** Usate un Large Language Model (come quello integrato in Cursor) per generare il boilerplate (codice iniziale, strutture di file, funzioni base). Non fatevi scrivere tutta l'app, ma usatelo per accelerare le parti noiose.

---

### **Setup Pre-Hackathon (Da fare prima di iniziare)**

1.  **Tutti:**
    *   Installate [Cursor](https://cursor.sh/), il vostro IDE collaborativo.
    *   Create un account GitHub se non lo avete.
    *   Ottenete le chiavi API necessarie. Saranno fondamentali e non potete perdere tempo a richiederle durante l'hackathon:
        *   **Chiave API per LLM:** Una chiave per OpenAI (GPT-4/GPT-3.5) o Google AI Studio (Gemini). Servirà per il chatbot.
        *   **Chiave API per Visione:** Cercate un'API di food recognition (es. Clarifai Food Model, Spoonacular). Avere un'API pronta vi farà risparmiare ore di lavoro.
2.  **Un responsabile del team:**
    *   Crea un nuovo repository su GitHub.
    *   Invita tutti i membri del team come collaboratori.
    *   Crea un branch `main` protetto (opzionale, ma buona pratica).
    *   Clonate tutti il repository.

---

### **GIORNO 1: Le Fondamenta (7 Ore)**

L'obiettivo di oggi è costruire la spina dorsale dell'applicazione e implementare la prima, cruciale, funzionalità AI.

#### **Mattina (3.5 Ore): Backend Core e Database Semplice**

*   **Obiettivo:** Avere un server API funzionante in grado di gestire utenti e dati glicemici.
*   **Git:** Iniziate tutti sul branch `main`. Create subito un branch `feature/backend-core`. Lavorerete tutti su questo branch per la mattinata.

**Piano d'azione:**
1.  **(Tutti insieme, 15 min):** Aprite un progetto in Cursor. Usate l'AI per generare la struttura base di un'applicazione **FastAPI** con un file `main.py`.
2.  **(Tutti insieme, 30 min):** Definite i modelli di dati usando Pydantic, direttamente nel codice. Vi serviranno almeno:
    *   `User(id, email, hashed_password)`
    *   `GlucoseReading(id, user_id, value, timestamp)`
    *   `Meal(id, user_id, description, carbs, timestamp, image_url)`
3.  **(Coppia A, 2.5 ore):** Implementate la logica del "database".
    *   **Hackathon-trick:** Non usate un vero database. Create un file `database.json` e scrivete semplici funzioni Python per leggere e scrivere su questo file. Sarà molto più veloce. `def save_data(data)`, `def load_data()`.
    *   Implementate gli endpoint API (CRUD) per le letture glicemiche:
        *   `POST /glucose` (per aggiungere una lettura)
        *   `GET /glucose/{user_id}` (per ottenere le letture di un utente)
4.  **(Coppia B, 2.5 ore):** Implementate l'autenticazione.
    *   Usate l'AI di Cursor per chiedere: "implement basic JWT token authentication in FastAPI".
    *   Create gli endpoint:
        *   `POST /register`
        *   `POST /login` (restituisce un token JWT)
    *   Create un sistema di "dipendenza" (`Depends`) in FastAPI per proteggere gli altri endpoint, assicurandovi che solo un utente autenticato possa aggiungere o leggere i *propri* dati.
5.  **(Tutti insieme, 15 min finali):**
    *   **Pull Request:** La persona che ha "guidato" di più il branch `feature/backend-core` apre una Pull Request (PR) verso `main`.
    *   **Code Review Veloce:** Tutti guardate il codice, commentate e approvate.
    *   **Merge!** Avete la vostra base funzionante su `main`.

---

#### **Pomeriggio (3.5 Ore): Stima Nutrizionale da Foto (AI #1)**

*   **Obiettivo:** Un endpoint che riceve un'immagine e restituisce una stima dei carboidrati.
*   **Git:** Create un nuovo branch da `main`: `feature/image-analysis`.

**Piano d'azione:**
1.  **(Coppia A, 3 ore):** Sviluppate il servizio di analisi.
    *   Create un nuovo file, es. `vision_service.py`.
    *   Scrivete una funzione che prende in input i byte di un'immagine.
    *   Questa funzione chiama l'API di food recognition che avete scelto (es. Clarifai) e ottiene una lista di alimenti riconosciuti (es. `['pasta', 'tomato', 'cheese']`).
    *   Trovate online un semplice file CSV o JSON con dati nutrizionali. Scrivete una funzione che mappa gli alimenti riconosciuti ai loro valori di carboidrati e li somma.
2.  **(Coppia B, 3 ore):** Create l'endpoint API e integrate.
    *   In FastAPI, create un nuovo endpoint `POST /meals/analyze`.
    *   Questo endpoint deve ricevere un upload di file (immagine).
    *   Deve chiamare la funzione sviluppata dalla Coppia A.
    *   Oltre alla stima, l'endpoint deve anche salvare il pasto nel vostro `database.json` (chiamando le funzioni del backend core) e associare l'URL dell'immagine (dovrete salvarla temporaneamente).
3.  **(Tutti insieme, 30 min finali):**
    *   **Test e Debug:** Testate l'endpoint con Postman o Insomnia. Assicuratevi che funzioni.
    *   **Pull Request:** Aprite una PR da `feature/image-analysis` a `main`.
    *   **Review e Merge:** Revisionate e unite il codice.

**Fine Giorno 1:** Avete un backend con autenticazione, salvataggio dati e una potente feature AI funzionante.

---

### **GIORNO 2: Intelligenza Conversazionale e Demo (7 Ore)**

L'obiettivo di oggi è dare una "voce" alla vostra app e creare una semplice interfaccia per mostrarne il potenziale.

#### **Mattina (3.5 Ore): Assistente Chatbot (AI #2)**

*   **Obiettivo:** Un endpoint di chat che permette all'utente di interrogare i propri dati in linguaggio naturale.
*   **Git:** Create un nuovo branch da `main`: `feature/chatbot`.

**Piano d'azione:**
1.  **(Tutti insieme, 30 min):** Progettate l'interazione.
    *   Decidete quali domande deve capire il bot (es. "qual è la mia glicemia media di oggi?", "quanti carboidrati ho mangiato a pranzo?").
    *   **Prompt Engineering:** Scrivete un "System Prompt" per l'LLM (GPT/Gemini). Sarà qualcosa del tipo:
        > "Sei Gluc.IA, un assistente per diabetici. Rispondi in modo conciso. Per rispondere, puoi usare i dati che ti fornirò. Non inventare mai valori. Se non sai la risposta, dì che non hai l'informazione."
2.  **(Coppia A, 3 ore):** Sviluppate la logica del Chatbot.
    *   Create un nuovo endpoint `POST /chat`.
    *   L'endpoint riceve il messaggio dell'utente.
    *   Recupera i dati rilevanti per quell'utente dal `database.json` (es. ultime 24 ore di glicemia, ultimi pasti).
    *   Formatta un prompt completo per l'LLM, che include il System Prompt, i dati recuperati e la domanda dell'utente.
    *   Invia il prompt all'API dell'LLM (OpenAI/Gemini).
    *   Restituisce la risposta dell'LLM all'utente.
3.  **(Coppia B, 3 ore):** Rifinite e testate.
    *   Mentre la coppia A implementa, voi testate i prompt direttamente nei playground delle API (es. OpenAI Playground) per vedere come risponde l'AI. Questo vi darà feedback rapido.
    *   Aiutate a "formattare" i dati da passare all'LLM in modo che siano chiari e facili da interpretare per la macchina.
    *   Integrate e debuggate insieme alla Coppia A.
4.  **(Tutti insieme, alla fine):**
    *   **Pull Request:** Aprite la PR da `feature/chatbot` a `main`.
    *   **Review e Merge:** Revisionate e unite.

---

#### **Pomeriggio (3.5 Ore): Frontend Mock e Integrazione Finale**

*   **Obiettivo:** Una singola pagina web (brutta ma funzionale) per dimostrare tutto il lavoro fatto.
*   **Git:** Create l'ultimo branch: `feature/frontend-mock`.

**Piano d'azione:**
1.  **(Tutti insieme, 30 min):** Usate l'AI di Cursor per generare una singola pagina `index.html`. Chiedete:
    > "Generate a single-page HTML file using Bootstrap CDN with a simple navigation bar, a section for 'Meal Analysis' with a file input and a button, and a section for 'Chat with Gluc.IA' with a text input and a chat window."
2.  **(Coppia A, 3 ore):** Cablate la logica della Stima Nutrizionale.
    *   Scrivete il codice JavaScript (all'interno di un tag `<script>` in `index.html`) per l'analisi del pasto.
    *   Usate `fetch()` per chiamare l'endpoint `POST /meals/analyze` quando l'utente carica un'immagine e clicca il pulsante.
    *   Mostrate il risultato (es. la stima dei carboidrati) sulla pagina.
3.  **(Coppia B, 3 ore):** Cablate la logica del Chatbot.
    *   Scrivete il codice JavaScript per la chat.
    *   Usate `fetch()` per chiamare l'endpoint `POST /chat` con il messaggio dell'utente.
    *   Appendete la domanda dell'utente e la risposta del bot nella finestra della chat.
4.  **(Tutti insieme, ultimi 30 min):**
    *   **Final Push & Demo Prep:** Sistemate gli ultimi bug. Assicuratevi che la demo funzioni dall'inizio alla fine.
    *   **Pull Request Finale:** Aprite l'ultima PR da `feature/frontend-mock` a `main`.
    *   **Merge Finale:** Congratulazioni, il vostro MVP è completo e su `main`! Preparatevi a presentarlo.
