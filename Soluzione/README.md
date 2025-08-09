# Fame – Diet Monitoring Web Application

Fame è un'applicazione web che ti consente di caricare la dieta fornita dal tuo nutrizionista, personalizzarla con le tue preferenze alimentari e generare un piano settimanale di pasti completo di lista della spesa. L'applicazione è pensata per essere responsive, quindi utilizzabile comodamente sia da desktop che da dispositivi mobili.

## Funzionalità principali

- **Registrazione e accesso**: ogni utente può creare un account personale indicando anche la propria regione (utile per suggerimenti legati ai prodotti tipici).
- **Upload dieta**: puoi caricare un file (testo o PDF) con la tua dieta. Il contenuto viene salvato nel database e utilizzato come base per generare i piani settimanali.
- **Preferenze**: puoi indicare cibi non graditi o allergie; queste informazioni saranno usate per evitare di proporti determinati alimenti nei piani.
- **Generazione piano settimanale**: premendo il pulsante “Generate Plan” viene creato un piano di pranzo e cena per ogni giorno della settimana successiva. Se è configurata una chiave API per Google Gemini, l'app interroga il modello per generare i pasti e la lista della spesa. In assenza di chiave, viene utilizzato un piano dimostrativo.
- **Lista della spesa via email**: al termine della generazione, la lista della spesa e il piano settimanale vengono inviati via email all'indirizzo registrato. Se non hai configurato un server di posta, il contenuto della mail sarà stampato a console.
- **Visualizzazione diete e piani**: nella dashboard puoi consultare l'ultima dieta caricata e l'ultimo piano generato.

## Requisiti

Assicurati di avere installato Python 3.10 o superiore. Per installare le dipendenze richieste, esegui:

```bash
pip install -r requirements.txt
```

Le principali librerie utilizzate sono:

- **Flask** – per il framework web;
- **Flask-SQLAlchemy** – per l'ORM e la gestione del database SQLite;
- **Flask-Login** – per l'autenticazione degli utenti;
- **Requests** – per l'eventuale chiamata all'API di Google Gemini.

## Configurazione

L'app legge la configurazione da variabili d'ambiente. Puoi impostare queste variabili nel tuo shell oppure creare un file `.env` e caricarlo manualmente. I parametri principali sono:

- `SECRET_KEY` – chiave segreta per la sessione Flask (obbligatoria in produzione).
- `DATABASE_URL` – URI del database. Di default viene creato un file `app.db` nella cartella dell'app.
- `GEMINI_API_KEY` – la chiave API per il modello Google Gemini. Se non la imposti, verrà restituito un piano di esempio.
- `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD` – parametri per inviare le email tramite SMTP. Se `MAIL_SERVER` non è impostato, le email saranno stampate a console.
- `PORT` – porta su cui avviare l'applicazione (default 5000).

Ad esempio, su Linux/macOS puoi esportare le variabili prima di avviare l'app:

```bash
export SECRET_KEY="metti-qui-una-chiave-sicura"
export GEMINI_API_KEY="la-tua-chiave-API-Gemini"
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USE_TLS="true"
export MAIL_USERNAME="tua-email@gmail.com"
export MAIL_PASSWORD="la-tua-password"
```

## Avvio in locale

Per avviare l'applicazione in locale, posizionati nella cartella `fame_app` ed esegui:

```bash
python app.py
```

L'app sarà raggiungibile all'indirizzo `http://localhost:5000`. Aprila in un browser e prova a registrarti, caricare la tua dieta e generare un piano. Poiché l'interfaccia è responsive, la potrai usare comodamente anche da smartphone.

## Esecuzione dei test

È stato incluso un set minimo di test automatici basati su `pytest` per verificare le funzionalità principali. Per eseguirli:

```bash
pip install pytest
pytest -q
```

I test utilizzano un database SQLite in memoria e non influiscono sui dati reali.

## Pubblicazione online

Per pubblicare l'applicazione online, puoi utilizzare un servizio di hosting di applicazioni Python, ad esempio [Render](https://render.com/), [Heroku](https://www.heroku.com/) o [Fly.io](https://fly.io/). In linea generale dovrai:

1. Inizializzare un repository Git nella directory `fame_app` e caricare il codice su GitHub o altro provider.
2. Creare un file `Procfile` (per Heroku) o configurare il `Dockerfile` per altri servizi. Per Heroku, il `Procfile` potrebbe contenere:
   
   ```Procfile
   web: gunicorn app:flask_app
   ```

   dove `flask_app` è la variabile creata in fondo a `app.py` quando l'app è eseguita come modulo.
3. Impostare le variabili d'ambiente nel pannello di configurazione del servizio (SECRET_KEY, GEMINI_API_KEY, dati SMTP ecc.).
4. Effettuare il deploy. Il servizio installerà automaticamente i pacchetti indicati in `requirements.txt` e avvierà l'app.

Assicurati che la porta utilizzata dall'app corrisponda a quella richiesta dal servizio di hosting (di solito Heroku usa la variabile d'ambiente `PORT`).

## Note sul modello Gemini

L'integrazione con Google Gemini è stata realizzata prevedendo l'endpoint `v1beta/models/gemini-pro:generateContent`. Nel codice troverai la funzione `call_gemini_api` in `utils.py`, che costruisce la richiesta e recupera la risposta. Se la variabile `GEMINI_API_KEY` non è impostata, la funzione restituisce un piano dimostrativo. Per utilizzare davvero il modello dovrai ottenere una chiave API valida da Google e impostarla come variabile d'ambiente.

## Struttura del progetto

```
fame_app/
├── app.py            # entry point Flask
├── config.py         # configurazione dell'app
├── models.py         # definizione dei modelli SQLAlchemy
├── utils.py          # funzioni di utilità (API Gemini, email, piano settimanale)
├── requirements.txt  # dipendenze Python
├── templates/        # file HTML basati su Jinja2
├── tests/            # test automatici
└── README.md         # questo file
```

## File statici e Bootstrap

La grafica fa uso di Bootstrap 5 caricato tramite CDN, quindi non è necessario scaricare altre librerie CSS o JS. Se vuoi personalizzare ulteriormente l'interfaccia, puoi aggiungere file CSS/JS nella cartella `static/` e includerli in `base.html`.

## Conclusioni

Questa applicazione fornisce un punto di partenza robusto per gestire un piano alimentare personalizzato. Puoi ampliarla integrando ulteriori funzionalità come il supporto alle notifiche push, l'esportazione del piano in PDF o la sincronizzazione con calendari esterni. Buon divertimento!