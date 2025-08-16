# 🚀 Istruzioni di Deploy per FAME

## 📋 Panoramica

FAME può essere deployato con un'architettura separata:
- **Frontend**: GitHub Pages (gratuito)
- **Backend**: Render.com, Heroku, Railway (gratuito/low-cost)

## 🌐 Deploy Frontend (GitHub Pages)

### 1. Prepara il Repository
```bash
# Fork questo repository su GitHub
# Clona il tuo fork
git clone https://github.com/TUOUSERNAME/FAME.git
cd FAME
```

### 2. Configura GitHub Pages
1. Vai nelle **Settings** del tuo repository
2. Scorri fino a **Pages**
3. Seleziona **Source**: Deploy from a branch
4. Seleziona **Branch**: `main` e **Folder**: `/docs`
5. Clicca **Save**

### 3. Personalizza la Configurazione
Modifica `docs/config.js`:
```javascript
// Sostituisci con l'URL del tuo backend
const BACKEND_URL = 'https://your-app-name.onrender.com';
const GITHUB_REPO = 'https://github.com/yourusername/FAME';
```

### 4. Aggiorna i Link
Nel `docs/index.html` e `README.md`, sostituisci:
- `yourusername` con il tuo username GitHub
- `your-app-name` con il nome della tua app backend

## 🖥️ Deploy Backend

### Opzione A: Render.com (Consigliato - Gratuito)

1. **Crea account** su [render.com](https://render.com)
2. **Connetti GitHub** e seleziona il repository FAME
3. **Crea Web Service** con queste impostazioni:
   ```
   Name: fame-backend
   Environment: Python
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **Aggiungi Environment Variables**:
   ```
   SECRET_KEY=your-super-secret-key-here
   FLASK_ENV=production
   ```

5. **Deploy**: Render farà automaticamente il deploy ad ogni push

### Opzione B: Heroku

1. **Installa Heroku CLI**
2. **Login**: `heroku login`
3. **Crea app**: `heroku create your-app-name`
4. **Configura variabili**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set FLASK_ENV=production
   ```
5. **Deploy**: `git push heroku main`

### Opzione C: Railway

1. **Connetti GitHub** su [railway.app](https://railway.app)
2. **Seleziona repository** FAME
3. **Aggiungi variabili** nel dashboard:
   - `SECRET_KEY`
   - `FLASK_ENV=production`
4. **Deploy automatico** ad ogni push

## 🔧 Configurazione CORS

Il backend è già configurato per accettare richieste da:
- `https://yourusername.github.io` (GitHub Pages)
- `http://localhost:3000` (sviluppo React)
- `http://localhost:5000` (sviluppo locale)

Aggiorna la configurazione CORS in `app.py`:
```python
CORS(app, origins=["https://your-actual-username.github.io", "http://localhost:3000", "http://localhost:5000"])
```

## 📧 Configurazione Email (Opzionale)

Per inviare liste della spesa via email, aggiungi queste variabili d'ambiente:

```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**Nota**: Per Gmail, usa una [App Password](https://support.google.com/accounts/answer/185833) invece della password normale.

## 🔍 Test del Deploy

### Frontend
1. Visita: `https://yourusername.github.io/FAME`
2. Verifica che la pagina si carichi correttamente
3. Controlla che il link "Prova la Demo" punti al tuo backend

### Backend
1. Visita: `https://your-app-name.onrender.com`
2. Dovresti vedere la homepage di FAME
3. Testa registrazione e login
4. Verifica che le API key personali funzionino

## 🐛 Troubleshooting

### Frontend non si carica
- Verifica che GitHub Pages sia abilitato
- Controlla che i file siano nella cartella `/docs`
- Aspetta fino a 10 minuti per la propagazione

### Backend errori 500
- Controlla i log del servizio di hosting
- Verifica che `SECRET_KEY` sia impostata
- Controlla che il database si crei correttamente

### CORS errors
- Verifica che l'URL frontend sia nella lista CORS
- Controlla che non ci siano typo negli URL
- Usa HTTPS per entrambi frontend e backend

### Database issues
- Il database SQLite viene creato automaticamente
- In produzione, considera PostgreSQL per performance migliori
- I servizi gratuiti potrebbero resettare il DB periodicamente

## 🔄 Aggiornamenti

### Frontend
- Modifica i file in `/docs`
- Commit e push: GitHub Pages si aggiorna automaticamente

### Backend  
- Modifica i file dell'app
- Commit e push: il servizio di hosting fa redeploy automatico

## 📊 Monitoraggio

### Render.com
- Dashboard con metriche CPU/memoria
- Log in tempo reale
- Alerting automatico

### Heroku
- CLI: `heroku logs --tail`
- Dashboard web con metriche
- Add-on per monitoring avanzato

## 💰 Costi

### Gratuito
- **GitHub Pages**: Completamente gratuito
- **Render.com**: 750 ore/mese gratuite
- **Railway**: $5 di credito mensile

### Upgrade Consigliati
- **Render Pro** ($7/mese): Database persistente, domini custom
- **Heroku Hobby** ($7/mese): SSL, metriche avanzate
- **Railway Pro** ($20/mese): Risorse dedicate

## 🔒 Sicurezza

- **Non committare mai** chiavi API nel codice
- **Usa variabili d'ambiente** per tutti i segreti
- **Abilita HTTPS** sempre in produzione
- **Limita CORS** solo ai domini necessari

## 📈 Scaling

Per traffico elevato, considera:
- **Database**: PostgreSQL invece di SQLite
- **Cache**: Redis per sessioni
- **CDN**: CloudFlare per assets statici
- **Load Balancer**: Multiple istanze backend
