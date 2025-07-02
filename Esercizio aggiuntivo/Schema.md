# **Hackathon di Estensione: FAME 2.0 – The Bio-Integrated Engine**

*Autore: Mirko Calcaterra*

*Estensione Proposta di Fame, esercizio di lunedì*

---

Benvenuti all'hackathon di estensione di FAME. Partirete tutti da una base di codice funzionante: la versione originale di FAME, un'app che genera piani alimentari e liste della spesa. Il vostro compito, come team, è di evolverla in **FAME 2.0**, un assistente nutrizionale dinamico che si integra con la vita reale dell'utente.

**Obiettivo principale:** Trasformare FAME da un generatore di piani statici a uno strumento che si **adatta quotidianamente** ai dati biometrici dell'utente.

**Metodologia:** Lavorerete in "vibe coding" su un unico repository. Ogni studente sarà "owner" di una delle seguenti Missioni. Questo significa che guiderà lo sviluppo di quella feature, ma tutti dovranno collaborare e integrare il proprio lavoro per far funzionare il prodotto finale.

---

### **Le Quattro Missioni di Sviluppo (Una per Studente)**

Ogni studente sceglierà una Missione. Sarete valutati sulla base del successo della vostra Missione e di come si integra con quelle degli altri.

#### **Missione 1: Il Ponte Biometrico (The Bio-Bridge)**

*   **Owner:** Studente A
*   **Obiettivo:** Far entrare i dati del mondo reale nell'applicazione. Devi creare un sistema che fornisca dati biometrici giornalieri simulati per ogni utente.

*   **Task Concreti:**
    1.  **Crea un Mock Data Provider:** Sviluppa un modulo Python (`biometric_provider.py`) che, dato un `user_id`, generi dati giornalieri realistici e **consistenti** (devono essere gli stessi se richiamati più volte per lo stesso utente e giorno). I dati da generare sono:
        *   `active_calories_burned` (calorie attive bruciate)
        *   `steps` (passi)
        *   `sleep_hours` (ore di sonno della notte precedente)
    2.  **Sviluppa l'Endpoint API:** Crea un nuovo endpoint protetto nel backend FastAPI, ad esempio `GET /users/me/biometrics`, che utilizzi il tuo provider per restituire i dati biometrici dell'utente autenticato per la giornata odierna in formato JSON.
    3.  **Visualizza i Dati nel Frontend:** Modifica la dashboard/home page di React per chiamare questo nuovo endpoint e visualizzare i dati biometrici in una piccola card "Il tuo report di oggi".

*   **Valutazione della Missione:**
    *   **Successo:** I dati biometrici sono generati, esposti tramite API e visibili nel frontend.
    *   **Eccellenza:** Il provider di dati mock è intelligente (es. i dati variano in modo plausibile giorno per giorno) e la visualizzazione nel frontend è chiara e immediata.

---

#### **Missione 2: L'Architetto del Prompt Adattivo (The Adaptive Prompt-Architect)**

*   **Owner:** Studente B
*   **Obiettivo:** Rendere l'IA "consapevole" dello stato fisico dell'utente. Devi modificare il cuore dell'app, ovvero la logica di generazione del piano alimentare, per includere i nuovi dati biometrici.

*   **Task Concreti:**
    1.  **Modifica la Logica di Generazione:** Intervieni sulla funzione `generate_mealplan()` nel backend. Prima di chiamare Gemini, questa funzione deve ora **chiamare l'endpoint della Missione 1** (`GET /users/me/biometrics`) per recuperare i dati del giorno.
    2.  **Ingegnerizza il Nuovo Prompt:** Riscrivi il prompt inviato a Gemini. Non devi solo aggiungere i nuovi numeri, ma devi "istruire" l'IA su *come* usarli. Esempio di prompt migliorato:
        > *"Sei un nutrizionista AI. Genera un piano per un utente con le seguenti preferenze: {{preferenze}}. Oggi l'utente ha uno stato fisico particolare: ha bruciato {{calorie}} kcal attive e ha dormito solo {{ore_sonno}} ore. Tieni conto di questo: aumenta l'apporto calorico per compensare l'attività fisica e suggerisci cibi che favoriscano il recupero e l'energia, data la scarsità di sonno. Restituisci il risultato in formato JSON..."*
    3.  **Crea un Punto di Attivazione:** Aggiungi un pulsante nel frontend, ad esempio sulla dashboard, con l'etichetta "Adatta il piano di domani". La pressione di questo pulsante deve scatenare la nuova logica di generazione del piano.

*   **Valutazione della Missione:**
    *   **Successo:** Il piano alimentare generato cambia visibilmente quando i dati biometrici sono diversi.
    *   **Eccellenza:** Il prompt è sofisticato e produce piani non solo quantitativamente diversi (più calorie), ma *qualitativamente* migliori (cibi per il recupero, ecc.), dimostrando una profonda comprensione del potenziale dell'LLM.

---

#### **Missione 3: L'Analista Nutrizionale (The Nutrition Analyst)**

*   **Owner:** Studente C
*   **Obiettivo:** Dare all'utente un feedback immediato e utile sull'impatto nutrizionale di ciò che mangia, collegandolo agli obiettivi.

*   **Task Concreti:**
    1.  **Traccia i Consumi Giornalieri:** Modifica il backend per salvare non solo il piano, ma anche lo "stato" di un pasto (es. `mangiato` / `saltato`). Aggiorna i modelli di dati e crea un endpoint `POST /meals/{meal_id}/consume`.
    2.  **Crea un Endpoint di Riepilogo:** Sviluppa un nuovo endpoint `GET /users/me/nutrition-summary` che calcoli e restituisca i totali nutrizionali (calorie, carboidrati, proteine, grassi) dei pasti consumati dall'utente nella giornata odierna.
    3.  **Sviluppa una Dashboard di Progresso:** Nel frontend, crea una nuova vista o una sezione nella home page chiamata "Progresso Giornaliero". Questa sezione deve:
        *   Chiamare l'endpoint di riepilogo.
        *   Mostrare i totali nutrizionali rispetto agli obiettivi dell'utente (es. `1800/2200 kcal`).
        *   Utilizzare barre di progresso o "anelli" per una visualizzazione chiara e immediata.

*   **Valutazione della Missione:**
    *   **Successo:** L'utente può segnare i pasti come consumati e vedere un riepilogo numerico dei suoi consumi giornalieri.
    *   **Eccellenza:** La dashboard di progresso è visivamente accattivante, interattiva e offre all'utente un feedback potente e motivante sui suoi obiettivi.

---

#### **Missione 4: Il Cronista della Settimana (The Weekly Chronicler)**

*   **Owner:** Studente D
*   **Obiettivo:** Dare all'utente una visione storica dei suoi progressi, trasformando i dati giornalieri in insight settimanali.

*   **Task Concreti:**
    1.  **Endpoint Dati Storici:** Crea un endpoint API `GET /users/me/weekly-report?date={{data}}` che aggreghi i dati delle **Missioni 1 e 3** su un arco di 7 giorni. L'endpoint deve restituire:
        *   La media giornaliera di calorie bruciate, passi e ore di sonno.
        *   La media giornaliera di calorie e macronutrienti consumati.
    2.  **Componente Grafico:** Sviluppa un nuovo componente React che utilizzi una libreria di grafici (es. `Recharts` o `Chart.js`).
    3.  **Pagina di Riepilogo Settimanale:** Crea una nuova pagina/rotta nel frontend chiamata "Report Settimanale". Questa pagina deve:
        *   Permettere all'utente di navigare tra le settimane (settimana corrente, settimana precedente).
        *   Chiamare l'endpoint dei dati storici.
        *   Usare il tuo componente grafico per visualizzare l'andamento dei dati chiave (es. un grafico a barre che confronta calorie bruciate vs. calorie consumate per ogni giorno della settimana).

*   **Valutazione della Missione:**
    *   **Successo:** L'utente può visualizzare un riepilogo numerico dei dati della settimana passata.
    *   **Eccellenza:** La visualizzazione grafica è chiara, interattiva e permette all'utente di identificare facilmente trend e pattern nel suo comportamento (es. "Vedo che nel weekend dormo di più ma consumo anche più calorie").

---
### **Valutazione Finale**

La valutazione terrà conto del completamento delle singole missioni, della qualità del codice prodotto e, soprattutto, del **successo dell'integrazione finale**. Un'app in cui tutte e quattro le missioni comunicano tra loro in modo fluido e creano un'esperienza utente coerente riceverà il punteggio più alto.
