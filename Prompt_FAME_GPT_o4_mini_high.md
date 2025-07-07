You are a senior full-stack engineer and AI specialist. Your task is to design and scaffold from scratch a production-ready, mobile-first web application called **FAME (Food AI Meal Engine)**, according to the following detailed requirements.

---

📌 **Project Overview**  
FAME è una web-app intelligente che trasforma in automatico le linee guida nutrizionali di un dietista in:
1. Un piano alimentare settimanale personalizzato (colazione, pranzo, merenda, cena – configurabili).  
2. Una lista della spesa ottimizzata per quantità, stagionalità e numero di persone in casa.  
3. Schede pasto con ricetta, valori nutrizionali e video-tutorial YouTube.

---

🔧 **Tech Stack & Tools**  
- **Backend**: Python + FastAPI, Uvicorn  
- **Frontend**: React (TypeScript), mobile-first, Tailwind CSS, shadcn/ui, React Big Calendar  
- **Database**: PostgreSQL (via SQLAlchemy + Alembic)  
- **Auth**: JWT stateless (python-jose[cryptography]), login/register, password recovery  
- **API keys & env** (gestiti con python-dotenv):
  - `GEMINI_API_KEY` → Google Generative AI (Gemini)
  - `YOUTUBE_API_KEY` → YouTube Data API v3
  - (Opzionale) `SPOONACULAR_KEY` → Spoonacular API
- **Google SDKs**:  
  - `google-generative-ai` per invocare Gemini con prompt parametrico → JSON  
  - `google-api-python-client` per YouTube Data API  
- **Altre librerie Python**: fastapi, uvicorn, sqlalchemy, alembic, python-jose[cryptography], pydantic, pytest  
- **CLI & DevOps**: git, Docker (facoltativo), render-cli per deploy su Render, Replit CLI  

---

⚙️ **Functional Requirements**  
1. **Onboarding** multi-step con sesso, età, peso, altezza, sport, allergie/intolleranze, obiettivo (massa/dimagrimento), membri famiglia, pasti da includere. Dati modificabili in Settings.  
2. **Home → Calendario**: vista settimanale drag & drop con React Big Calendar. Azioni FAB:  
   - Carica dieta (PDF/image → OCR)  
   - Prenota consulto (link esterno NutriDoc)  
   - Genera piano  
3. **Generazione piano**: chiamata a Gemini con prompt parametrico, ricezione JSON strutturato, filtraggio per stagionalità (calendario UE), obbligo di rispettare allergie e target calorico/macronutrienti, salvataggio in DB, rendering nel calendario.  
4. **Scheda Pasto**: titolo, descrizione, ingredienti (grammatura scalata), istruzioni passo-passo, valori nutrizionali, link YouTube video-tutorial.  
5. **Lista della Spesa**: aggregazione ingredienti a livello settimanale, raggruppati per reparto supermercato, esportabili in PDF/CSV.  
6. **Settings**: profilo utente, preferenze alimentari, numero persone, target peso/massa, API-keys.

---

📐 **Non-Functional Requirements**  
- **Prompt Engineering**: scrivi i template dei prompt con variabili dinamiche, poi gestisci la post-elaborazione JSON su backend.  
- **Testing**:  
  - Unit tests (pytest) per logica di generazione e post-processing  
  - Integration tests (FastAPI TestClient)  
  - E2E tests con Playwright o Cypress (login, onboarding, generazione piano, drag&drop, export lista).  
- **Quality**: linting (flake8/isort, ESLint, Prettier), type-checking (mypy, TS).  
- **CI/CD**: GitHub Actions o Render Build Hooks, test + build + deploy automatico.  
- **Containerization**: Dockerfile per backend, Docker Compose opzionale.  

---

🚀 **Deployment**  
- **Render** (render-cli): 2 servizi (web backend + static frontend) + managed PostgreSQL.  
- **Replit** (replit deployments) come alternativa gratuita.  

---

🎯 **Deliverables**  
1. **Repo skeleton** con monorepo o due cartelle (`/backend`, `/frontend`).  
2. **File di configurazione**: `pyproject.toml`, `requirements.txt`, `tsconfig.json`, `tailwind.config.js`, `.eslintrc.js`, `docker-compose.yml` (opzionale), `Dockerfile`.  
3. **Esempio `.env.example`** con tutte le chiavi:  

GEMINI_API_KEY=
YOUTUBE_API_KEY=
SPOONACULAR_KEY=
DATABASE_URL=postgresql://user:pass@localhost:5432/fame
JWT_SECRET_KEY=

4. **Codice di base** per ciascun modulo (autenticazione, onboarding, calendario, generazione, scheda pasto, lista spesa, settings).  
5. **Template di prompt** LLM parametrico (in `backend/app/prompts/`).  
6. **Configurazione CI/CD** per testing e deploy.  
7. **E2E test suite** di esempio.  

> **Istruzioni per Lovable Dev:**  
> - Usa questo prompt in modalità “Scaffold full-stack app”.  
> - Fai leva su best practice di architettura e DevOps.  
> - Genera commenti inline per spiegare ogni cartella/file.  
> - Includi esempi di prompt engineering e post-processing JSON.  
> - Fornisci anche uno script di deploy su Render.