# BLUEPRINT: A Cool Timer with a Face

> A retro 8-bit fitness countdown timer featuring colour-coded urgency feedback and pixel-art facial expressions — because your reps deserve a face.

---

## Overview

**BLUEPRINT** is a full-stack countdown timer application built for fitness enthusiasts, interval trainers, and anyone who wants a bit of personality injected into their rest periods. As the clock winds down, the timer's pixel-art avatar reacts with progressively urgent facial expressions and the background shifts through a colour spectrum — from calm green to panicked red — giving you an at-a-glance urgency signal without ever needing to read the numbers.

**Who it's for:**
- Athletes and gym-goers timing rest intervals or AMRAP sets
- Coaches running group workouts
- Developers looking for a reference implementation of a FastAPI + React/Vite + in-memory state architecture
- Anyone who thinks a timer should have feelings

**Key Features:**
- 🕹️ Retro 8-bit pixel-art facial avatar with dynamic expressions
- 🎨 Colour-coded background urgency bar (green → yellow → red)
- ⌨️ Keyboard shortcut support for hands-free control
- ⚡ FastAPI backend managing timer state in-memory
- ⚛️ React/Vite frontend with TypeScript throughout
- 🧪 Full test coverage on both backend and frontend

---

## Technology Stack

| Layer | Technology | Notes |
|---|---|---|
| Primary Language | Python 3.x | Backend runtime |
| Backend Framework | FastAPI | REST API, in-memory timer state |
| Frontend Framework | React (with TypeScript) | Vite-powered dev/build toolchain |
| Frontend Build Tool | Vite | Fast HMR, TSX support |
| Language (Frontend) | TypeScript | Strict typing via `tsconfig.json` |
| Styling | CSS Modules / Global CSS | Pixel-art aesthetics, animations |
| Testing (Backend) | pytest | Unit + router-level tests |
| Testing (Frontend) | Vitest / Testing Library | Component and hook tests |
| Package Manager (FE) | npm | `package-lock.json` present |
| Containerisation | None | Run locally |

---

## Architecture

BLUEPRINT follows a clean **client–server** split with two top-level runtime environments:

```
Browser (React/Vite)  ←→  HTTP/REST  ←→  FastAPI Server (Python)
```

### Backend (`app/`)

The FastAPI application is structured around three layers:

- **Routers** (`app/routers/timers.py`) — HTTP route definitions; thin controllers that delegate to services.
- **Services** (`app/services/`) — Business logic. `timer_service.py` orchestrates timer lifecycle (start, pause, reset, tick). `urgency_calculator.py` is a pure function module that derives urgency level from remaining time and total duration.
- **Repository** (`app/repos/timer_repo.py`) — An in-memory data store abstracting state reads/writes. No external database is required.
- **Models** (`app/models/timer.py`) — Pydantic models defining the timer data schema.
- **Config** (`app/config.py`) — Environment-driven configuration loaded via `app/dependencies.py`.

### Frontend (`web/`)

The React application is composed of:

- **`web/src/components/`** — UI building blocks:
  - `FacialAvatar.tsx` — The 8-bit pixel-art face; expression changes with urgency level.
  - `BackgroundBar.tsx` — Full-screen urgency colour feedback layer.
  - `TimerDisplay.tsx` — Formatted countdown readout.
  - `TimerContainer.tsx` — Orchestrates layout.
  - `DurationPicker.tsx`, `StartPauseButton.tsx`, `ResetButton.tsx` — Controls.
- **`web/src/hooks/`** — Custom React hooks:
  - `useTimer.ts` — Polls/syncs timer state with the backend.
  - `useUrgencyStyle.ts` — Derives CSS variables/classes from urgency level.
  - `useKeyboardShortcuts.ts` — Maps keyboard events to timer actions.
- **`web/src/api/timerApi.ts`** — Typed HTTP client wrapping all backend calls.
- **`web/src/types/timer.ts`** — Shared TypeScript type definitions mirroring backend models.

---

## Project Structure

```
BLUEPRINT/
├── app/                          # FastAPI backend
│   ├── main.py                   # Application entry point, CORS, router registration
│   ├── config.py                 # Settings and environment loading
│   ├── dependencies.py           # FastAPI dependency injection providers
│   ├── models/
│   │   └── timer.py              # Pydantic timer model
│   ├── repos/
│   │   └── timer_repo.py         # In-memory timer state repository
│   ├── routers/
│   │   └── timers.py             # /timers API routes
│   └── services/
│       ├── timer_service.py      # Timer lifecycle logic
│       └── urgency_calculator.py # Urgency level computation
│
├── tests/                        # Backend test suite (pytest)
│   ├── test_timer_service.py
│   ├── test_timers_router.py
│   └── test_urgency_calculator.py
│
├── web/                          # React/Vite frontend
│   ├── index.html                # Vite HTML entry point
│   ├── vite.config.ts            # Vite configuration (proxy to backend)
│   ├── tsconfig.json             # TypeScript configuration
│   ├── package.json
│   └── src/
│       ├── main.tsx              # React root mount
│       ├── App.tsx               # Top-level component
│       ├── api/
│       │   └── timerApi.ts       # Backend HTTP client
│       ├── components/           # All UI components
│       ├── hooks/                # Custom React hooks
│       ├── styles/               # Global CSS and animations
│       ├── tests/                # Frontend unit tests
│       └── types/
│           └── timer.ts          # Shared TypeScript types
│
├── .env.example                  # Environment variable template
├── requirements.txt              # Python dependencies
└── forge_plan.json               # Project blueprint/plan metadata
```

---

## Setup & Installation

### Prerequisites

- Python **3.9+** with `pip`
- Node.js **18+** with `npm`
- A terminal and a love of pixel art

### 1. Clone the Repository

```bash
git clone <repository-url>
cd BLUEPRINT
```

### 2. Backend Setup

```bash
# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

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

### Start the Backend

From the project root (with your virtual environment active):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The FastAPI server will be available at `http://localhost:8000`.  
Interactive API docs: `http://localhost:8000/docs`

### Start the Frontend

In a separate terminal:

```bash
cd web
npm run dev
```

The Vite dev server will be available at `http://localhost:5173` and will proxy API calls to the backend automatically (configured in `vite.config.ts`).

### Production Build (Frontend)

```bash
cd web
npm run build
# Output in web/dist/
```

---

## Environment Variables

Copy `.env.example` to `.env` and populate the following keys before running the backend:

| Variable | Description | Required |
|---|---|---|
| `APP_HOST` | Host address the FastAPI server binds to | No (default: `0.0.0.0`) |
| `APP_PORT` | Port the FastAPI server listens on | No (default: `8000`) |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins | Yes |
| `DEBUG` | Enable debug/reload mode (`true`/`false`) | No (default: `false`) |

> ⚠️ Never commit your `.env` file. It is listed in `.gitignore`.

---

## API Routes

All routes are prefixed under the FastAPI application registered in `app/routers/timers.py`.

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/timers/{timer_id}` | Retrieve current timer state |
| `POST` | `/timers` | Create a new timer with a specified duration |
| `POST` | `/timers/{timer_id}/start` | Start or resume the timer |
| `POST` | `/timers/{timer_id}/pause` | Pause the running timer |
| `POST` | `/timers/{timer_id}/reset` | Reset the timer to its initial duration |
| `DELETE` | `/timers/{timer_id}` | Delete a timer from in-memory state |

> Full interactive documentation with request/response schemas is available at `http://localhost:8000/docs` when the backend is running.

---

## Testing

### Backend Tests (pytest)

From the project root with your virtual environment active:

```bash
pytest tests/ -v
```

Test files:

| File | Coverage |
|---|---|
| `tests/test_timer_service.py` | Timer lifecycle logic (start, pause, reset, tick) |
| `tests/test_timers_router.py` | HTTP route integration tests |
| `tests/test_urgency_calculator.py` | Urgency level computation edge cases |

### Frontend Tests (Vitest)

```bash
cd web
npm run test
```

Test files:

| File | Coverage |
|---|---|
| `web/src/tests/useTimer.test.ts` | Timer hook state and sync behaviour |
| `web/src/tests/useUrgencyStyle.test.ts` | CSS urgency derivation logic |
| `web/src/tests/FacialAvatar.test.tsx` | Avatar expression rendering |

### Run All Tests

```bash
# Backend
pytest tests/ -v

# Frontend (in separate terminal)
cd web && npm run test
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes with clear messages: `git commit -m "feat: add blinking animation to avatar"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request describing your changes

Please ensure all existing tests pass and add new tests for any new functionality before submitting.

---

## License

This project is licensed under the [MIT License](LICENSE).

> © BLUEPRINT Contributors. Pixel faces not included in liability.