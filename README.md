# BLUEPRINT: A Cool Timer with a Face

> A retro 8-bit fitness countdown timer featuring colour-coded urgency feedback and expressive pixel-art facial reactions — powered by FastAPI and React/Vite.

---

## Overview

**BLUEPRINT** is a full-stack fitness countdown timer application that brings personality to your workouts. As time ticks down, the interface responds with dynamic colour shifts indicating urgency levels and animated pixel-art facial expressions that react to your remaining time — keeping you motivated and entertained through every rep, set, and rest period.

### Who It's For

- Fitness enthusiasts who want a more engaging workout timer
- Developers looking for a fun, full-stack reference project combining FastAPI and React
- Anyone who appreciates retro 8-bit aesthetics in their productivity tools

### Key Features

- ⏱️ Countdown timer with configurable durations
- 🎨 Colour-coded urgency feedback (e.g., green → yellow → red as time runs out)
- 👾 Pixel-art facial expressions that change based on timer state
- 🧠 In-memory timer state managed by a FastAPI backend
- ⚡ Fast, responsive React/Vite frontend

---

## Technology Stack

| Layer        | Technology          | Notes                            |
|--------------|---------------------|----------------------------------|
| Language     | Python 3.10+        | Backend runtime                  |
| Backend      | FastAPI             | REST API & in-memory state       |
| Frontend     | React + Vite        | UI, animations, pixel-art faces  |
| Database     | PostgreSQL          | Persistent storage (optional)    |
| Styling      | CSS / Tailwind CSS  | Retro 8-bit pixel aesthetic      |
| HTTP Client  | Axios / Fetch API   | Frontend ↔ Backend communication |
| ASGI Server  | Uvicorn             | Serves the FastAPI application   |

---

## Architecture

BLUEPRINT follows a classic client-server architecture with a clear separation between the React frontend and the FastAPI backend.

```
┌─────────────────────────────────────────────────────┐
│                    Browser Client                    │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           React / Vite Frontend              │   │
│  │                                              │   │
│  │  ┌────────────┐   ┌────────────────────┐    │   │
│  │  │ Timer UI   │   │ Pixel Face Engine  │    │   │
│  │  │ (Countdown)│   │ (Expression Logic) │    │   │
│  │  └────────────┘   └────────────────────┘    │   │
│  │                                              │   │
│  │  ┌──────────────────────────────────────┐   │   │
│  │  │      Colour Urgency Controller       │   │   │
│  │  └──────────────────────────────────────┘   │   │
│  └──────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP / REST (JSON)
┌──────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                      │
│                                                      │
│  ┌──────────────┐   ┌──────────────────────────┐    │
│  │ Timer Routes │   │  In-Memory State Manager │    │
│  │ /api/timer/* │   │  (active timers, status) │    │
│  └──────────────┘   └──────────────────────────┘    │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │            PostgreSQL (optional)             │   │
│  │        Persisted timer history/config        │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### Component Descriptions

| Component                   | Responsibility                                                                 |
|-----------------------------|--------------------------------------------------------------------------------|
| **React Frontend**          | Renders the timer UI, pixel-art face, and colour urgency states                |
| **Timer UI**                | Displays the countdown, start/stop/reset controls                              |
| **Pixel Face Engine**       | Selects and renders the correct 8-bit facial expression based on timer state   |
| **Colour Urgency Controller** | Maps remaining time percentage to a colour scale (green → yellow → red)      |
| **FastAPI Backend**         | Exposes REST endpoints, manages in-memory timer state, handles business logic  |
| **In-Memory State Manager** | Tracks active timer sessions, durations, and current status                   |
| **PostgreSQL**              | Optional persistent layer for saving timer presets and historical session data |

---

## Project Structure

```
blueprint/
├── backend/
│   ├── main.py                  # FastAPI app entry point
│   ├── routers/
│   │   └── timer.py             # Timer API route definitions
│   ├── models/
│   │   └── timer.py             # Pydantic models / DB schemas
│   ├── services/
│   │   └── timer_service.py     # In-memory state & business logic
│   ├── database.py              # PostgreSQL connection (optional)
│   └── requirements.txt         # Python dependencies
│
├── frontend/
│   ├── public/
│   │   └── sprites/             # 8-bit pixel-art face sprite assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── Timer.jsx        # Main countdown timer component
│   │   │   ├── PixelFace.jsx    # Pixel-art facial expression renderer
│   │   │   └── UrgencyBar.jsx   # Colour-coded urgency indicator
│   │   ├── hooks/
│   │   │   └── useTimer.js      # Custom hook for timer state/logic
│   │   ├── services/
│   │   │   └── api.js           # Axios/Fetch API calls to backend
│   │   ├── styles/
│   │   │   └── retro.css        # 8-bit pixel-art styling
│   │   ├── App.jsx              # Root application component
│   │   └── main.jsx             # Vite entry point
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── .env.example                 # Environment variable template
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Prerequisites

Ensure you have the following installed:

- **Python** 3.10 or higher
- **Node.js** 18 or higher & **npm** / **yarn**
- **PostgreSQL** (optional — only required for persistent storage)
- **Git**

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/blueprint.git
cd blueprint
```

---

### 2. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Copy the environment variable template
cp ../.env.example ../.env
# Edit .env with your configuration values
```

---

### 3. Frontend Setup

```bash
# Navigate to the frontend directory
cd ../frontend

# Install Node dependencies
npm install
```

---

### 4. Database Setup (Optional)

If using PostgreSQL for persistence:

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE blueprint;"

# Run migrations (if applicable)
cd ../backend
alembic upgrade head
```

---

## Usage / Running

### Start the Backend

```bash
cd backend
source venv/bin/activate        # On Windows: venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The FastAPI server will be available at: `http://localhost:8000`  
Interactive API docs (Swagger UI): `http://localhost:8000/docs`  
ReDoc documentation: `http://localhost:8000/redoc`

---

### Start the Frontend

```bash
cd frontend
npm run dev
```

The React application will be available at: `http://localhost:5173`

---

### Production Build (Frontend)

```bash
cd frontend
npm run build
# Compiled output will be in frontend/dist/
```

---

## Environment Variables

Copy `.env.example` to `.env` in the project root and configure the following variables:

| Variable                  | Description                                               | Required |
|---------------------------|-----------------------------------------------------------|----------|
| `DATABASE_URL`            | PostgreSQL connection string                              | Optional |
| `BACKEND_HOST`            | Host address for the FastAPI server                       | Yes      |
| `BACKEND_PORT`            | Port for the FastAPI server (default: `8000`)             | Yes      |
| `CORS_ORIGINS`            | Comma-separated list of allowed frontend origins          | Yes      |
| `SECRET_KEY`              | Application secret key for session/token signing          | Yes      |
| `DEBUG`                   | Enable debug mode (`true` / `false`)                      | No       |
| `VITE_API_BASE_URL`       | Base URL for frontend API calls (e.g. `http://localhost:8000`) | Yes |
| `MAX_TIMER_DURATION`      | Maximum allowed timer duration in seconds                 | No       |
| `DEFAULT_TIMER_DURATION`  | Default countdown duration in seconds                     | No       |

> ⚠️ **Never commit your `.env` file to version control.** It is included in `.gitignore` by default.

---

## API Routes

All backend routes are prefixed with `/api`.

### Timer Endpoints

| Method   | Endpoint                    | Description                                      |
|----------|-----------------------------|--------------------------------------------------|
| `GET`    | `/api/timer`                | Retrieve all active timer sessions               |
| `GET`    | `/api/timer/{timer_id}`     | Retrieve a specific timer by ID                  |
| `POST`   | `/api/timer`                | Create and start a new countdown timer           |
| `PATCH`  | `/api/timer/{timer_id}`     | Update timer state (pause, resume, reset)        |
| `DELETE` | `/api/timer/{timer_id}`     | Delete / cancel a timer session                  |

### Health Check

| Method | Endpoint    | Description                  |
|--------|-------------|------------------------------|
| `GET`  | `/health`   | Backend health check         |

### Example Request — Create Timer

```json
POST /api/timer
Content-Type: application/json

{
  "duration": 60,
  "label": "Push-up set",
  "auto_start": true
}
```

### Example Response

```json
{
  "id": "abc-123",
  "label": "Push-up set",
  "duration": 60,
  "remaining": 60,
  "status": "running",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Install test dependencies (if not already installed)
pip install pytest pytest-asyncio httpx

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend

# Run unit tests (Vitest)
npm run test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### End-to-End Tests

```bash
# Install Playwright (if using E2E tests)
npx playwright install

# Run E2E tests
npx playwright test
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature-name`
3. **Commit** your changes: `git commit -m "feat: add your feature