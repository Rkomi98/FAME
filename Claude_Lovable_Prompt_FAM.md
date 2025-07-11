Prompt per Lovable - FAME App

## Descrizione del Progetto
Crea **FAME** (Food AI Meal Engine), una web-app mobile-first per la generazione di piani alimentari personalizzati con AI. L'app deve trasformare le linee guida nutrizionali in menu settimanali, liste della spesa e video ricette.

## Stack Tecnologico
- **Frontend**: React + TypeScript + Tailwind CSS + shadcn/ui
- **Backend**: FastAPI + Python
- **Database**: SQLAlchemy
- **AI**: Google Gemini per generazione menu
- **API**: YouTube Data API per video ricette
- **Design**: Mobile-first, responsive

## Funzionalità Principali

### 1. Sistema di Autenticazione
- Login/Register con email + password
- JWT per autenticazione stateless
- Recupero password
- Logout sicuro

### 2. Onboarding Multi-Step
Al primo accesso, questionario con:
- Dati personali: sesso, età, peso, altezza
- Attività sportiva praticata e frequenza settimanale
- Allergie e intolleranze alimentari
- Numero membri famiglia
- Obiettivo: dimagrire/mettere massa/mantenimento
- Pasti da includere: colazione, pranzo, merenda, cena
- Frequenza promemoria idratazione (ogni 1-4 ore)

### 3. Dashboard Principale (Home)
- Vista calendario settimanale con pasti generati
- Drag & drop per riorganizzare i pasti
- **FAB (Floating Action Button)** in basso a destra con 3 opzioni:
  1. 📄 "Carica dieta" (upload PDF/immagine)
  2. 👩‍⚕️ "Prenota consulto" (link esterno)
  3. ✨ "Genera piano" (AI generation)

### 4. Generazione Piano AI
- Form con preferenze specifiche
- Integrazione Google Gemini
- Filtro ingredienti stagionali
- Rispetto allergie e obiettivi calorici
- Salvataggio automatico su database

### 5. Scheda Pasto Dettagliata
Per ogni pasto:
- Titolo e descrizione
- Lista ingredienti con grammature
- Istruzioni passo-passo
- Link YouTube alla ricetta
- Valori nutrizionali (calorie, macro)
- Foto del piatto

### 6. Lista della Spesa
- Aggregazione automatica ingredienti settimanali
- Raggruppamento per reparto supermercato
- Scaling quantità in base a numero persone
- Export PDF/CSV
- Checkbox per spuntare prodotti acquistati

### 7. Impostazioni Utente
- Modifica profilo e preferenze
- Gestione allergie/intolleranze
- Numero persone in casa
- Target peso/massa
- Preferenze pasti (orari, tipologie)
- Configurazione promemoria idratazione

### 8. Sistema Promemoria Idratazione
- Notifiche push personalizzabili
- Pop-up in-app per ricordare di bere
- Tracker consumo acqua giornaliero
- Statistiche settimanali idratazione
- Personalizzazione frequenza (1-4 ore)
- Pausa notifiche durante sonno

## Design Requirements

### UI/UX
- **Mobile-first**: ottimizzato per smartphone
- **Design moderno**: palette colori vivaci, gradients
- **Animazioni fluide**: transizioni tra schermate
- **Glassmorphism**: effetti vetro per card e modali
- **Dark mode**: supporto tema scuro/chiaro
- **Accessibilità**: contrasti adeguati, testi leggibili

### Componenti Specifici
- **Calendar view**: griglia settimanale con pasti
- **Stepper**: per onboarding multi-step
- **Cards**: per pasti e ricette
- **Bottom sheet**: per azioni rapide
- **Loading states**: skeleton screens durante AI generation
- **Toast notifications**: feedback azioni utente
- **Hydration popup**: promemoria bere con animazioni
- **Progress rings**: tracker acqua giornaliero

### Layout
- **Header**: logo + hamburger menu
- **Navigation**: bottom tab bar con icone
- **FAB**: floating action button principale
- **Cards grid**: layout pasti e ricette
- **Full screen**: dettagli pasto e lista spesa

## Integrazione Backend

### API Endpoints
```
POST /auth/login
POST /auth/register
POST /auth/forgot-password
GET /user/profile
PUT /user/profile
POST /mealplan/generate
GET /mealplan/weekly
GET /mealplan/meal/{id}
GET /shopping-list
POST /shopping-list/export
```

### Database Models
- User (id, email, password_hash, created_at)
- Profile (user_id, age, weight, height, allergies, goals, workout_frequency, hydration_frequency)
- MealPlan (id, user_id, week_start, meals_json)
- Meal (id, title, description, ingredients, instructions, youtube_link, nutrition)
- HydrationLog (id, user_id, date, glasses_count, target_glasses)

## Funzionalità Avanzate

### AI Integration
- Prompt engineering per Gemini
- Post-processing JSON response
- Fallback per errori AI
- Cache risultati per performance

### Stagionalità
- Calendario ingredienti UE
- Filtro automatico per mese corrente
- Suggerimenti prodotti locali

### Social Features (Nice-to-have)
- Condivisione piani alimentari
- Rating ricette
- Community recipes

## Performance & Ottimizzazioni
- Lazy loading immagini
- Caching API calls
- Offline mode per piani salvati
- Progressive Web App (PWA)
- Image optimization

## Deliverables
1. **Frontend React**: app mobile-first completa
2. **Backend FastAPI**: API robuste e sicure
3. **Database**: schema ottimizzato
4. **Documentazione**: API docs + user manual
5. **Deploy**: configurazione Render/Replit
6. **Testing**: test end-to-end principali flussi

## Priorità Sviluppo
1. **Core**: Auth + Onboarding + Dashboard
2. **AI**: Generazione piani + integrazione Gemini
3. **Features**: Lista spesa + schede pasto
4. **Polish**: UI/UX + performance + deploy

Crea un'app moderna, intuitiva e performante che renda la pianificazione alimentare un'esperienza piacevole e personalizzata!
