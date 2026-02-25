# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.9 | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 | https://nodejs.org/en/download |
| A terminal (Windows Command Prompt) | Built into Windows | Press `Win + R`, type `cmd`, press Enter |

**How to check if these are already installed:**
Open Command Prompt and type the following commands one at a time:
```
python --version
node --version
npm --version
```
Each command should print a version number. If you see an error instead, install that software using the links above.

---

## 2. Install

These steps download all the code libraries that BLUEPRINT needs to run. You only need to do this once.

**Step 1 — Install Python dependencies (the backend)**

Open Command Prompt, navigate to the main project folder (the one that contains `requirements.txt`), and run:
```
pip install -r requirements.txt
```
Wait for it to finish. You may see a lot of text scrolling — that is normal.

**Step 2 — Install JavaScript dependencies (the frontend)**

Still in Command Prompt, navigate into the `web` folder inside the project:
```
cd web
npm install
```
Wait for it to finish, then go back to the main project folder:
```
cd ..
```

---

## 3. Credential / API Setup

No external credentials required.

BLUEPRINT runs entirely on your own computer. It does not connect to any third-party services, payment systems, or online accounts. No sign-ups or API keys are needed.

---

## 4. Configure .env

The `.env` file is a plain text file that holds settings for the application. Think of it as a short list of preferences the program reads when it starts.

**Create your `.env` file by running this command** from the main project folder:
```
copy .env.example .env
```
This copies the example settings file into a working settings file called `.env`. You can open it with Notepad if you wish to change any values.

**List of all settings:**

| Variable | What It Does | Required? | Default Value |
|---|---|---|---|
| `CORS_ORIGINS` | Tells the backend which web addresses are allowed to talk to it. Normally you do not need to change this. | Optional | `http://localhost:5173,http://localhost:3000` |
| `DEFAULT_DURATION_SECONDS` | Sets how many seconds the timer starts at when you first open the app. Change this if you prefer a different starting time (e.g., `30` for 30 seconds, `300` for 5 minutes). | Optional | `60` |
| `JWT_SECRET` | A private password used internally to secure communication. For personal/local use the default is fine. If others can access your network, change this to something random. | Optional | `your-secret-key-here` |
| `DATABASE_URL` | A database address. BLUEPRINT uses in-memory storage, so **this setting is not used** and can be left as-is. | Optional | `postgresql://user:password@localhost:5432/timers` |

For most users, simply copying `.env.example` to `.env` and leaving everything at its defaults is all you need to do.

---

## 5. Run

**Starting the application (recommended — one command):**

From the main project folder in Command Prompt, run the boot script:
```
boot.bat
```
This single command starts both the backend (FastAPI) and the frontend (React) together.

**After a few seconds**, open your web browser and go to:
```
http://localhost:5173
```
You should see the BLUEPRINT retro timer interface.

**Starting each part manually (if `boot.bat` does not work):**

Open **two separate** Command Prompt windows.

*Window 1 — Start the backend:*
```
python -m uvicorn app.main:app --reload
```

*Window 2 — Start the frontend (navigate to the `web` folder first):*
```
cd web
npm run dev
```
Then open `http://localhost:5173` in your browser.

---

## 6. Stop

**If you used `boot.bat`:**
Click on the Command Prompt window that is running and press:
```
Ctrl + C
```
Press `Y` and then `Enter` if it asks you to confirm. This shuts down both the backend and the frontend.

**If you started them in two separate windows:**
Click each Command Prompt window one at a time and press `Ctrl + C` in each one.

It is safe to close the Command Prompt windows after pressing `Ctrl + C`.

---

## 7. Key Settings Explained

| Setting | Plain-language explanation |
|---|---|
| `DEFAULT_DURATION_SECONDS` | This is the number of seconds shown on the timer when the page first loads. Set it to `30` for a 30-second timer, `120` for 2 minutes, etc. |
| `CORS_ORIGINS` | A security rule that controls which browser addresses can communicate with the backend. If you open the app on a different port or address, add it here separated by a comma. Most users never need to touch this. |
| `JWT_SECRET` | Think of this like a house key — it is used to lock and verify internal messages. For personal use on your own computer, the default value is fine. If you deploy this for others to use, replace it with a long random string of letters and numbers. |
| `DATABASE_URL` | A placeholder address for a database. BLUEPRINT stores timer data in memory while it is running, so this setting currently has no effect. |
| Port `5173` | The "door number" your browser uses to reach the timer app. This is set automatically by the frontend and does not need to be changed. |
| Port `8000` | The "door number" the backend API listens on. This is the default for the Python server and also does not need to be changed under normal use. |

---

## 8. Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python is not installed or not added to your system PATH | Reinstall Python from https://www.python.org/downloads/ and **tick the box that says "Add Python to PATH"** during installation |
| `'npm' is not recognized as an internal or external command` | Node.js is not installed or not added to PATH | Reinstall Node.js from https://nodejs.org/en/download — it adds itself to PATH automatically |
| Browser shows `This site can't be reached` at `http://localhost:5173` | The frontend is not running | Make sure you ran `boot.bat` or started the frontend manually with `npm run dev` inside the `web` folder |
| `pip install` fails with `No module named pip` | pip is missing from your Python installation | Run `python -m ensurepip --upgrade` in Command Prompt, then try again |
| Timer data disappears when the server restarts | Expected behaviour — BLUEPRINT uses in-memory storage | This is normal. The app does not save timers to disk. Simply set your timer again after restarting. |
| `Address already in use` error on startup | Another program (or a previous run) is already using port `8000` or `5173` | Close any other Command Prompt windows running the app, or restart your computer to free up the ports, then try again |