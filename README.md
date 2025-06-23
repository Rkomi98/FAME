# FAME - Webapp AI per Piani Alimentari Settimanali
*Autore: Mirko Calcaterra*

## Introduzione e Obiettivi

**FAME** (**F**ood **A**I **M**eal **E**ngine) è una webapp intelligente che, data una dieta fornita da un nutrizionista, genera automaticamente un piano alimentare settimanale completo e la relativa lista della spesa. L'applicazione è concepita per essere mobile-friendly (accessibile da smartphone) e utilizza un backend Python con un modello di intelligenza artificiale (Google Gemini LLM) per capire la dieta e produrre i pasti settimanali e gli ingredienti necessari. Al termine, il progetto verrà distribuito gratuitamente su Render (PaaS cloud).

### Obiettivi Didattici
Questa guida fornisce istruzioni passo-passo per completare il progetto in circa 4 ore di laboratorio, suddiviso in sessioni da 30-60 minuti. Gli studenti impareranno a:
- Collaborare in team (4 persone) usando strumenti moderni (Replit, GitHub) e metodologie AI-assisted (vibe coding).
- Configurare i prerequisiti tecnici (ambienti di sviluppo e account API cloud).
- Suddividere il lavoro in frontend, backend, AI integration e deploy in modo efficiente.
- Sviluppare una webapp full-stack: interfaccia utente semplice (anche generata con strumenti AI come Lovable), backend API in Python (FastAPI/Flask) con integrazione di modelli AI (Google Gemini) e di servizi esterni (YouTube Data API per arricchire il piano con contenuti multimediali).
- Scrivere prompt efficaci per interpretare la dieta e generare un piano alimentare settimanale adeguato.
- Eseguire test end-to-end e fare il deploy su Render (utilizzando la versione gratuita) seguendo le best practices per un'implementazione fluida.

Al termine del laboratorio, gli studenti avranno realizzato una webapp funzionante in grado di ricevere le linee guida di una dieta personalizzata e restituire un menu settimanale variegato, completo di lista della spesa e (opzionalmente) link a ricette video da YouTube, il tutto pronto per essere utilizzato su dispositivi mobili.

## Prerequisiti e Setup Iniziale
Prima di iniziare la lezione pratica, assicurarsi di aver soddisfatto i seguenti prerequisiti:
- **Account Replit:** Piattaforma online con IDE integrato. Supporta oltre 50 linguaggi, collaborazione in tempo reale e include la funzionalità AI "Ghostwriter". Non è necessario installare nulla localmente.
- **Editor/IDE con AI (Cursor):** In alternativa a Replit, si può installare Cursor, un IDE basato su VS Code con assistente AI integrato.
- **Account Lovable:** Strumento di sviluppo AI-driven che genera codice sorgente da descrizioni in linguaggio naturale, ideale per prototipare front-end.
- **Account GitHub:** Necessario per la collaborazione e il controllo di versione. Si consiglia di creare un repository privato e aggiungere i collaboratori.
- **Account Google Cloud Platform (GCP):** Necessario per abilitare le seguenti API:
  - **API Google Gemini (Generative AI):** Per generare i piani alimentari. È necessario abilitare l'API e ottenere una API Key.
  - **YouTube Data API v3:** Per cercare video di ricette. Abilitare l'API e creare una API Key dedicata.
- **Librerie e tool da installare:**
  - Python 3.10+ (disponibile su Replit).
  - FastAPI (o Flask) e Uvicorn.
  - SDK `google-generative-ai` (o in alternativa la libreria `vertex-ai` o `requests`).
  - Google API Python Client (`google-api-python-client`).
  - Git (se si lavora in locale).
  - Render CLI (opzionale).

## Istruzioni Iniziali e Metodologia ("Vibe Coding")

### Divisione dei Ruoli (4 studenti)
La teoria per un progetto del genere vorrebbe che venissero designati 4 ruoli come di seguito:
- **Studente 1 - Frontend Developer:** Responsabile dell'interfaccia utente (HTML/CSS/JS). Utilizzerà Lovable per la prototipazione rapida e garantirà la responsività per smartphone.
- **Studente 2 - Backend Developer:** Responsabile del server Python (FastAPI/Flask). Crea le rotte API, gestisce l'integrazione con Google Gemini e YouTube API e formatta la risposta per il frontend.
- **Studente 3 - Prompt Engineer & AI Specialist:** Si concentra sull'elaborazione dei prompt per il modello generativo (Gemini) per ottenere output corretti e strutturati. Collabora con il Backend Developer per integrare le richieste AI nel codice.
- **Studente 4 - DevOps & Testing:** Coordinatore per integrazione, versioning e deployment. Configura il repository GitHub, gestisce le chiavi API in sicurezza e guida il processo di deploy su Render.

Nella pratica ragazzi il mio consiglio è di lavorare in parallelo su Frontend e Backend almeno. I primi prompt "generali" vi consiglio addirittura di farli insieme, poi vi dividete in base alle feature che decidete di elaborare. L'obiettivo è quello di avere un'app production ready entro la fine della giornata che fa quanto discusso sopra. La "bellezza" viene a posteriori.

Spero di essermi spiegato.

Per lavorare ricordatevi di creare un repo con git e sfruttarlo al massimo. Confrontatevi in fase di merge.

### Metodologia "Vibe Coding"
Il "vibe coding" consiste nel descrivere la funzionalità desiderata in linguaggio naturale all'AI, che genererà il codice da testare e rifinire. Questo approccio permette di concentrarsi sull'idea piuttosto che sulla sintassi, accelerando lo sviluppo. È fondamentale, tuttavia, capire e verificare il codice generato dall'AI. Usatela, sarà il vostro boost :)!

## Timeline e Fasi del Laboratorio (4 Ore)
Per l'applicazione ho pensato di lavorare in python ma non siete costretti, anzi. Potenzialmente ogni linguaggio che permette di creare questo tipo di webapp è ben accetto.

### Sessione 1 (0:00 - 0:15) - Setup e Pianificazione
- **Impostazione ambiente condiviso:** Creare un repository GitHub e, se si usa Replit, collegarlo a un nuovo Repl Python.
- **Struttura iniziale del progetto:** Creare le cartelle `backend/` e `frontend/`, e i file `main.py`, `requirements.txt`, e `.gitignore`.
- **Divisione compiti dettagliata:** Decidere il framework (FastAPI è consigliato) e il formato di comunicazione front-back (es. JSON).
- **Setup credenziali:** Utilizzare la sezione "Secrets" di Replit o un file `.env` (da aggiungere a `.gitignore`) per le chiavi API `GOOGLE_API_KEY` e `YOUTUBE_API_KEY`.
- **Conferma funzionamento ambiente:** Creare un endpoint "Hello World" in FastAPI per verificare che il server parta correttamente.
  ```python
  # main.py
  from fastapi import FastAPI
  app = FastAPI()
  
  @app.get("/")
  async def root():
      return {"message": "FAME backend attivo"}
  ```

### Sessione 2 (0:15 - 1:30) - Prototipo Frontend & Scheletro Backend
Di seguito alcuni suggerimenti sul "cosa fare". Siete liberi di seguire questa struttura o di proporre una nuova. Partire da un buon prompt su lovable o altro tool online è sicuramente una buona cosa.

> *Chi ben inizia è a metà dell'opera*

- **Frontend (Studente 1):**
  - Usare Lovable.dev per generare un prototipo di pagina web descrivendo l'interfaccia desiderata. Siete in 4, sfruttate questa cosa per arginare i limiti dell'account gratuito di Lovable. Formulate in modo chiaro tramite prompt cosa volete generare, il linguaggio dell'applicazione e le feature che volete implementare. Le pagine che volete includere anche sono importanti.
  - Adattare il codice generato per inviare una richiesta `POST` a `/genera_piano` al click del bottone.
  - Integrare i file HTML/CSS/JS nel progetto e servirli tramite FastAPI.
  - Testare il layout e l'interattività della pagina.
- **Backend (Studente 2):**
  - Aggiungere le librerie necessarie a `requirements.txt`.
  - Implementare la rotta `POST /genera_piano` che accetta i dati della dieta e restituisce un JSON di placeholder.
    ```python
    from pydantic import BaseModel

    class DietaInput(BaseModel):
        dieta: str

    @app.post("/genera_piano")
    async def genera_piano(input: DietaInput):
        # Logica da implementare
        return {"piano": "Work in progress", "lista": ""}
    ```
  - Abilitare CORS se necessario.
- **Prompt Engineering (Studente 3):**
  - Elaborare un prompt efficace per l'LLM, specificando il contesto (assistente nutrizionista AI), le linee guida della dieta e il formato di output desiderato (es. JSON con chiavi "piano" e "lista_spesa").
  - Sperimentare e affinare il prompt usando la console di Google AI Studio o uno script Python per assicurarsi che l'output sia coerente e completo.

### Sessione 3 (1:30 - 2:30) - Integrazione AI nel Backend e Funzione Generativa
- **Implementazione chiamata a Google Gemini (Studente 2 & 3):**
  - Integrare l'SDK Python `google-generativeai` nel backend.
  - Configurare la chiave API all'avvio dell'app.
  - Implementare la logica nella rotta `genera_piano` per chiamare il modello Gemini con il prompt e il testo della dieta.
    ```python
    # Dentro la funzione genera_piano
    prompt = f"Sei un nutrizionista AI... {input.dieta}"
    try:
        response = genai.generate_text(prompt=prompt, model="models/text-bison-001")
        output_text = response.generations[0].text
        # Parsare l'output
        piano, lista = parse_output(output_text)
        return {"piano": piano, "lista": lista}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Errore generazione piano AI")
    ```
  - Scrivere una funzione `parse_output` per estrarre il piano e la lista della spesa dalla risposta dell'AI, gestendo sia JSON che testo formattato.
- **Integrazione YouTube Data API (Opzionale, Studente 4):**
  - Dopo aver generato il piano, è possibile arricchirlo con link a video di ricette.
  - Implementare una funzione che, dato il nome di un piatto, effettua una ricerca su YouTube tramite l'API e restituisce l'URL del primo video.