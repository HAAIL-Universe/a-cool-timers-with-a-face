# A cool timers with a Face

A real-time timer application with urgency-aware visual feedback, smooth animations, keyboard shortcuts, and a modern React frontend backed by a Python FastAPI server.

## Features

- **Urgency-Aware Colors**: Timer display changes color based on remaining time (safe → warning → critical)
- **Critical Pulse Animation**: When urgency level is critical (<10% remaining), the background pulses visibly
- **Smooth Transitions**: Color transitions between urgency zones are animated (500ms CSS transition)
- **Keyboard Shortcuts**: 
  - `Space` — Toggle start/pause
  - `R` — Reset the timer
- **Duration Presets**: Quick-select buttons for 15s, 30s, 45s, and 60s timers
- **Responsive UI**: Works on desktop and mobile browsers

## Prerequisites

- **Python 3.12+** (backend)
- **Node.js 18+** (frontend)
- **PostgreSQL 13+** (database)
- **Docker & Docker Compose** (optional, for containerized deployment)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd a-cool-timers-with-a-face
```

### 2. Backend Setup

#### Create Python Virtual Environment

```bash
# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (CMD)
python -m venv .venv
.venv\Scripts\activate.bat

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Install Backend Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Configure Environment Variables

Create a `.env` file at the project root with the following variables:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/timers_db
JWT_SECRET=your-secret-key-here-min-32-chars
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

See [Environment Variables](#environment-variables) section below for details.

#### Initialize Database

```bash
# Create the PostgreSQL database (if not already created)
createdb timers_db

# Run migrations (if applicable)
python -c "from app.repos.db import init_db; init_db()"
```

#### Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API will be available at `http://localhost:8000`

**API Documentation:** `http://localhost:8000/docs` (Swagger UI)

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd web
npm install
```

#### Configure Frontend Environment

Create a `.env` file in the `web/` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

#### Start Frontend Development Server

```bash
npm run dev
```

Frontend will be available at `http://localhost:5173` (or the URL shown in terminal)

#### Build Frontend for Production

```bash
npm run build
```

Output will be in `web/dist/`

## Running Tests

### Backend Tests

```bash
pytest -x
```

Run tests with verbose output:

```bash
pytest -xvs
```

### Frontend Tests

```bash
cd web
npm test
```

Watch mode for frontend tests:

```bash
cd web
npm test -- --watch
```

## Project Structure

```
.
├── README.md                 ← Project documentation (this file)
├── requirements.txt          ← Python backend dependencies
├── .env                      ← Environment variables (user-created)
├── .env.example              ← Template for environment variables
├── app/                      ← FastAPI backend
│   ├── main.py              ← Application entry point
│   ├── config.py            ← Settings & configuration
│   ├── dependencies.py       ← FastAPI dependency injection
│   ├── models/              ← Pydantic data models
│   ├── routers/             ← API route handlers
│   ├── services/            ← Business logic layer
│   └── repos/               ← Data access layer
├── tests/                    ← Backend tests
├── web/                      ← React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx          ← Root React component
│   │   ├── components/      ← Reusable React components
│   │   ├── hooks/           ← Custom React hooks
│   │   ├── styles/          ← CSS files
│   │   └── services/        ← API client functions
│   ├── public/              ← Static assets
│   ├── package.json         ← Frontend dependencies
│   ├── vite.config.ts       ← Vite build config
│   └── tsconfig.json        ← TypeScript config
└── Forge/                    ← Build governance (can be deleted post-build)
    ├── Contracts/           ← Project specifications
    └── evidence/            ← Build audit logs
```

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | Yes | PostgreSQL connection string | `postgresql://user:pass@localhost:5432/timers_db` |
| `JWT_SECRET` | Yes | Secret key for JWT token signing (min 32 chars) | `your-super-secret-key-at-least-32-characters-long` |
| `CORS_ORIGINS` | Yes | Comma-separated list of allowed CORS origins | `http://localhost:3000,http://localhost:5173` |
| `VITE_API_BASE_URL` | Yes (frontend) | Backend API base URL for frontend | `http://localhost:8000` |

## Running the Full Stack

### Option 1: Manual Start (Recommended for Development)

**Terminal 1 — Backend:**

```bash
source .venv/bin/activate  # or your platform's activation command
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**

```bash
cd web
npm run dev
```

### Option 2: Docker Compose (Production-like)

```bash
docker-compose up --build
```

Backend will run on `http://localhost:8000`, frontend on `http://localhost:3000`.

## Troubleshooting

### Backend Issues

**"ModuleNotFoundError: No module named 'app'"**
- Ensure you have activated the virtual environment: `. .venv/bin/activate`
- Run `pip install -r requirements.txt` again

**"psycopg2 compilation error"**
- On macOS: `brew install libpq`
- On Linux: `sudo apt-get install libpq-dev python3-dev`
- Then retry: `pip install psycopg2-binary`

**"DATABASE_URL not found"**
- Create `.env` file at project root with the required variables (see [Environment Variables](#environment-variables))

**PostgreSQL connection refused**
- Verify PostgreSQL is running: `pg_isready -h localhost`
- Check DATABASE_URL credentials and database name
- Create database if needed: `createdb timers_db`

### Frontend Issues

**"VITE_API_BASE_URL is not set"**
- Create `.env` file in `web/` directory (not at project root)
- Set `VITE_API_BASE_URL=http://localhost:8000`

**"Cannot GET /api/timers"**
- Verify backend is running on the configured API_BASE_URL
- Check CORS_ORIGINS includes your frontend URL

**Tests fail with "Cannot find module"**
- Run `npm install` again in the `web/` directory
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`

## Key Keyboard Shortcuts

- **Space** — Start/pause the timer
- **R** — Reset the timer to initial duration

## API Endpoints (Backend)

All endpoints are prefixed with `/api/timers`.

- `POST /create` — Create a new timer
- `GET /{timer_id}` — Fetch timer state
- `POST /{timer_id}/start` — Start the timer
- `POST /{timer_id}/stop` — Pause the timer
- `POST /{timer_id}/reset` — Reset the timer

For full API documentation, visit `http://localhost:8000/docs` when the backend is running.

## Development Notes

- Backend auto-reloads on file changes (thanks to `--reload` flag in `uvicorn`)
- Frontend hot-reloads via Vite's dev server
- Tests are deterministic and do not depend on live network calls
- TypeScript is type-checked during the build process

## License

[Add license information here if applicable]

## Support

For issues or questions, please open an issue on the repository.
