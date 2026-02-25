# BLUEPRINT: A Cool Timer with a Face

> A retro 8-bit fitness countdown timer with urgency-driven colour and facial expression feedback — because every rep deserves a reaction.

---

## Overview

**BLUEPRINT** is a retro-styled fitness countdown timer that brings personality to your workout intervals. As time ticks down, the interface reacts: background colours shift from calm greens to urgent reds, and an 8-bit pixel avatar changes its facial expression to match the intensity of the moment — relaxed when you have plenty of time, stressed when the clock is almost up.

### Who It's For

- Fitness enthusiasts who want a more engaging interval timer
- Developers looking for a clean FastAPI + React/TypeScript full-stack reference project
- Anyone who thinks timers should have feelings

---

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| **Language (Backend)** | Python 3.11+ | Primary backend language |
| **Backend Framework** | FastAPI | REST API, async-ready |
| **Frontend Framework** | React 18+ | Component-based UI |
| **Frontend Language** | TypeScript | Strict typing throughout |
| **Build Tool** | Vite | Fast dev server and bundler |
| **Styling** | CSS (custom) | Retro 8-bit aesthetic, CSS animations |
| **Testing (Backend)** | pytest | Unit and integration tests |
| **Testing (Frontend)** | Vitest / React Testing Library | Component and hook tests |
| **Containerisation** | None | Runs directly on host |

---

## Architecture

BLUEPRINT follows a clean three-layer architecture separated into two runtimes — a Python backend and a React frontend — communicating over a REST API.

```
┌─────────────────────────────────────────────┐
│               React Frontend (web/)          │
│                                             │
│  TimerContainer                             │
│  ├── FacialAvatar   (urgency expression)    │
│  ├── TimerDisplay   (MM:SS countdown)       │
│  ├── BackgroundBar  (colour urgency fill)   │
│  ├── DurationSelector                       │
│  ├── StartPauseButton                       │
│  └── ResetButton                            │
│                                             │
│  Hooks: useTimer · useKeyboard              │
│  API:   timerApi.ts  ──────────────────────►│
└────────────────────────┬────────────────────┘
                         │ HTTP REST
┌────────────────────────▼────────────────────┐
│               FastAPI Backend (app/)         │
│                                             │
│  routers/timers.py   (HTTP route handlers)  │
│  services/timer_service.py  (business logic)│
│  repos/timer_repo.py        (data access)   │
│  models/timer.py            (Pydantic models│
│  config.py                  (settings)      │
│  dependencies.py            (DI wiring)     │
└─────────────────────────────────────────────┘
```

### Component Descriptions

| Component | Responsibility |
|---|---|
| `routers/timers.py` | HTTP endpoint definitions; thin layer delegating to services |
| `services/timer_service.py` | Core timer business logic: create, tick, pause, reset |
| `repos/timer_repo.py` | In-memory (or future persistent) timer state storage |
| `models/timer.py` | Pydantic request/response schemas |
| `config.py` | App-wide settings loaded from environment |
| `dependencies.py` | FastAPI dependency injection providers |
| `FacialAvatar.tsx` | 8-bit pixel face that reacts to remaining time percentage |
| `BackgroundBar.tsx` | Full-width urgency colour bar (green → yellow → red) |
| `useTimer.ts` | Client-side polling / countdown hook wired to the API |
| `useKeyboard.ts` | Keyboard shortcut bindings (space to start/pause, `r` to reset) |

---

## Project Structure

```
.
├── app/                        # FastAPI backend
│   ├── main.py                 # Application entry point & CORS setup
│   ├── config.py               # Environment-based configuration
│   ├── dependencies.py         # Dependency injection
│   ├── models/
│   │   └── timer.py            # Pydantic timer models
│   ├── repos/
│   │   └── timer_repo.py       # Timer state repository
│   ├── routers/
│   │   └── timers.py           # /timers API routes
│   └── services/
│       └── timer_service.py    # Timer business logic
│
├── tests/                      # Backend test suite (pytest)
│   ├── test_timer_service.py
│   └── test_timers_router.py
│
├── web/                        # React/TypeScript frontend
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── main.tsx            # React entry point
│       ├── App.tsx             # Root application component
│       ├── index.css           # Global base styles
│       ├── animations.css      # Keyframe animations
│       ├── api/
│       │   └── timerApi.ts     # Typed API client
│       ├── components/         # All UI components
│       ├── hooks/              # useTimer, useKeyboard
│       ├── types/
│       │   └── timer.ts        # Shared TypeScript types
│       └── tests/              # Frontend unit tests
│
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
└── forge_plan.json             # Project blueprint/plan
```

---

## Setup & Installation

### Prerequisites

- Python **3.11+**
- Node.js **18+** and npm (or pnpm / yarn)
- Git

### 1. Clone the Repository

```bash
git clone <repository-url>
cd blueprint
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your values (see Environment Variables section)
```

### 3. Frontend Setup

```bash
cd web
npm install
cd ..
```

---

## Usage / Running

### Run the Backend (FastAPI)

```bash
# From the project root, with the virtual environment active
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs`

### Run the Frontend (React / Vite)

```bash
cd web
npm run dev
```

The UI will be available at `http://localhost:5173` (Vite default).

### Run Both Concurrently

Open two terminal windows and run the backend and frontend commands above simultaneously. The frontend is pre-configured to proxy API requests to `http://localhost:8000`.

---

## Environment Variables

Copy `.env.example` to `.env` and populate the values before running the application.

| Variable | Description | Required |
|---|---|---|
| `APP_ENV` | Runtime environment (`development`, `production`) | Yes |
| `ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | Yes |
| `API_HOST` | Host address for the FastAPI server | No |
| `API_PORT` | Port for the FastAPI server | No |
| `LOG_LEVEL` | Logging verbosity (`debug`, `info`, `warning`, `error`) | No |

> **Never commit your `.env` file.** It is listed in `.gitignore` by default.

---

## API Routes

Base URL: `http://localhost:8000`

| Method | Path | Description |
|---|---|---|
| `GET` | `/timers` | List all active timers |
| `POST` | `/timers` | Create a new timer |
| `GET` | `/timers/{timer_id}` | Retrieve a specific timer's state |
| `PATCH` | `/timers/{timer_id}/start` | Start or resume a timer |
| `PATCH` | `/timers/{timer_id}/pause` | Pause a running timer |
| `PATCH` | `/timers/{timer_id}/reset` | Reset a timer to its original duration |
| `DELETE` | `/timers/{timer_id}` | Delete a timer |

Full interactive API documentation is available via Swagger UI at `/docs` or ReDoc at `/redoc` when the backend is running.

---

## Testing

### Backend Tests (pytest)

```bash
# From the project root, with virtual environment active
pytest tests/ -v
```

```bash
# With coverage report
pytest tests/ -v --cov=app --cov-report=term-missing
```

Key test files:

| File | Coverage |
|---|---|
| `tests/test_timer_service.py` | Timer service business logic |
| `tests/test_timers_router.py` | API endpoint integration tests |

### Frontend Tests (Vitest)

```bash
cd web
npm run test
```

```bash
# Watch mode during development
npm run test -- --watch
```

Key test files:

| File | Coverage |
|---|---|
| `web/src/tests/FacialAvatar.test.tsx` | Avatar expression rendering |
| `web/src/tests/TimerDisplay.test.tsx` | Time formatting and display |
| `web/src/tests/useKeyboard.test.ts` | Keyboard shortcut hook behaviour |

---

## Contributing

Contributions are welcome! To get started:

1. **Fork** the repository and create a feature branch (`git checkout -b feature/my-feature`)
2. Make your changes, ensuring all existing tests pass
3. Add tests for any new functionality
4. Run the full test suite (backend + frontend) before submitting
5. Open a **Pull Request** with a clear description of your changes

Please follow existing code style conventions and keep commits focused and descriptive. For major changes, open an issue first to discuss the proposed approach.

---

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for full details.

---

*Built with ❤️ and a pixel-art stress face.*