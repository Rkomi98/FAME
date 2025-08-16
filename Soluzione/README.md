# FAME - Food and Meal Enhancement 🍽️

![Python](https://img.shields.io/badge/python-v3.10+-blue.svg)
![Flask](https://img.shields.io/badge/flask-v3.0+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-orange.svg)

**FAME** è un'applicazione web intelligente che trasforma la tua dieta del nutrizionista in piani settimanali personalizzati, completi di ricette stagionali e liste della spesa. Con supporto per allenamenti, preferenze alimentari e integrazione con i migliori modelli AI del mercato.

## ✨ Nuove Funzionalità

### 🔑 API Key Personali
- **Ogni utente usa la propria chiave API** - nessun costo condiviso!
- Supporto per **Google Gemini**, **OpenAI** e **Anthropic Claude**
- Configurazione durante la registrazione

### 🏋️ Integrazione Allenamenti
- Specifica se ti alleni, frequenza e giorni della settimana
- **Piani adattati automaticamente**: carboidrati prima dell'allenamento, proteine dopo
- Calcolo nutrizionale ottimizzato per sportivi

### 🌱 Stagionalità Garantita
- **Solo frutta e verdura di stagione** per la tua regione
- Ricette autentiche basate su fonti web verificate
- Rispetto della tradizione culinaria locale

### 🗑️ Gestione Dinamica dei Pasti
- **Elimina singoli pasti** dal piano settimanale
- Aggiornamento automatico della visualizzazione
- Flessibilità totale nella pianificazione

## 🚀 Demo Live

- **Frontend**: [https://tuonome.github.io/FAME](https://tuonome.github.io/FAME) *(GitHub Pages)*
- **Backend**: [https://fame-backend.onrender.com](https://fame-backend.onrender.com) *(Render.com)*

## 📋 Requisiti di Sistema

- **Python**: 3.10 o superiore
- **Chiave API**: Almeno una tra Gemini, OpenAI o Claude
- **Browser**: Moderno con supporto ES6+

## 🛠️ Installazione Rapida

### 1. Clona il Repository
```bash
git clone https://github.com/tuonome/FAME.git
cd FAME/Soluzione
```

### 2. Crea Ambiente Virtuale
```bash
python -m venv FAME
source FAME/bin/activate  # Linux/macOS
# FAME\Scripts\activate   # Windows
```

### 3. Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 4. Configura Ambiente (Opzionale)
Crea un file `.env` per lo sviluppo locale:
```bash
SECRET_KEY=your-secret-key-here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### 5. Avvia l'Applicazione
```bash
python app.py
```

Visita: `http://localhost:5000`

## 🔐 Configurazione API Key

Durante la registrazione, scegli il tuo provider AI preferito:

### Google Gemini (Consigliato)
- **Costo**: Gratuito fino a 15 richieste/minuto
- **Ottieni la chiave**: [Google AI Studio](https://aistudio.google.com/app/apikey)
- **Modelli supportati**: Gemini 1.5 Flash, Gemini 1.5 Pro

### OpenAI
- **Costo**: Pay-per-use (~$0.002 per piano)
- **Ottieni la chiave**: [OpenAI Platform](https://platform.openai.com/api-keys)
- **Modelli supportati**: GPT-3.5 Turbo, GPT-4

### Anthropic Claude
- **Costo**: Pay-per-use (~$0.003 per piano)
- **Ottieni la chiave**: [Anthropic Console](https://console.anthropic.com/)
- **Modelli supportati**: Claude 3 Sonnet

## 🌐 Deploy in Produzione

### Frontend (GitHub Pages)

1. **Fork il repository** su GitHub
2. **Abilita GitHub Pages** nelle impostazioni del repo
3. **Configura il branch** `gh-pages` come sorgente
4. **Personalizza** il file `config.js` con l'URL del tuo backend

### Backend (Render.com - Gratuito)

1. **Connetti il repository** su [Render.com](https://render.com)
2. **Crea un Web Service** con queste impostazioni:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```
3. **Aggiungi le variabili d'ambiente**:
   ```
   SECRET_KEY=your-production-secret-key
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   ```

### Alternative Backend
- **Heroku**: Con Procfile incluso
- **Railway**: Deploy automatico da Git
- **Fly.io**: Con Dockerfile
- **DigitalOcean App Platform**: Deploy one-click

## 📱 Utilizzo

### 1. Registrazione
- Crea account con username, email e password
- **Seleziona il provider AI** (Gemini/OpenAI/Claude)
- **Inserisci la tua chiave API personale**
- Specifica la tua regione per ingredienti stagionali

### 2. Configurazione Profilo
- **Preferenze alimentari**: Allergie e cibi da evitare
- **Allenamento**: Frequenza, giorni della settimana
- **Regione**: Per ingredienti locali e stagionali

### 3. Carica la Dieta
- **Upload PDF o testo** della dieta del nutrizionista
- Supporto per file multipagina e formati misti

### 4. Genera Piano Settimanale
- **Un click** per generare pranzo e cena per 7 giorni
- **Lista spesa automatica** categorizzata e quantificata
- **Invio email** con piano completo

### 5. Gestisci i Pasti
- **Visualizza dettagli** di ogni pasto (ingredienti, preparazione)
- **Elimina pasti singoli** se non graditi
- **Rigenera piano** quando necessario

## 🏗️ Architettura Tecnica

### Backend (Flask)
```
app.py              # Main Flask application
├── models.py       # SQLAlchemy database models
├── utils.py        # AI integration & utilities
├── config.py       # Configuration management
└── templates/      # Jinja2 HTML templates
```

### Database Schema
```sql
User:
- id, username, email, password
- region, api_provider, api_key
- trains, training_frequency, training_days
- favorite_emails, created_at

Plan:
- id, user_id, start_date
- content, json_content, shopping_list
- created_at
```

### API Integration
- **Multi-provider support**: Gemini, OpenAI, Claude
- **Automatic fallback**: Se un provider fallisce
- **Rate limiting**: Gestione automatica dei limiti
- **Error handling**: Graceful degradation

## 🧪 Test

```bash
# Installa pytest
pip install pytest

# Esegui tutti i test
pytest tests/ -v

# Test con coverage
pytest --cov=. tests/
```

## 🤝 Contribuire

1. **Fork** il progetto
2. **Crea un branch** per la feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** le modifiche (`git commit -m 'Add AmazingFeature'`)
4. **Push** al branch (`git push origin feature/AmazingFeature`)
5. **Apri una Pull Request**

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi `LICENSE` per dettagli.

## 🆘 Supporto

- **Issues**: [GitHub Issues](https://github.com/tuonome/FAME/issues)
- **Documentazione**: [Wiki del progetto](https://github.com/tuonome/FAME/wiki)
- **Email**: support@fame-app.com

## 🎯 Roadmap

- [ ] **Mobile App** (React Native)
- [ ] **Export PDF** dei piani settimanali  
- [ ] **Integrazione calendario** (Google Calendar, Outlook)
- [ ] **Analisi nutrizionale** avanzata
- [ ] **Community recipes** e condivisione
- [ ] **API pubblica** per sviluppatori

---

**Sviluppato con ❤️ per semplificare la tua alimentazione quotidiana**