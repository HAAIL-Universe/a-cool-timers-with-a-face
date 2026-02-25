# User Instructions

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click the links to download each one if you do not already have them.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.10 or higher | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 or higher | https://nodejs.org/en/download |
| A modern web browser | Any recent version | e.g., Chrome, Firefox, Edge |

**How to check if these are already installed:**

Open Command Prompt (press `Windows Key + R`, type `cmd`, press Enter) and run:

```
python --version
node --version
npm --version
```

Each command should print a version number. If you see an error instead, that software needs to be installed.

---

## 2. Install

You will run two sets of installation commands — one for the backend (Python/FastAPI) and one for the frontend (React). Open Command Prompt and navigate to the folder where you saved the project first.

> **Tip:** To navigate to a folder in Command Prompt, type `cd` followed by the folder path. For example: `cd C:\Users\YourName\Downloads\blueprint`

**Step 1 — Install backend dependencies** (run this from the main project folder):

```
pip install -r requirements.txt
```

Wait for this to finish. You will see several packages downloading and installing.

**Step 2 — Install frontend dependencies** (run this from the `web` subfolder):

```
cd web
npm install
cd ..
```

Wait for this to finish as well. This may take a minute or two.

---

## 3. Credential / API Setup

No external credentials required.

BLUEPRINT runs entirely on your local computer. You do not need to create any accounts, obtain any API keys, or sign up for any external services.

---

## 4. Configure .env

The `.env` file is a plain text file that stores settings for the application. You need to create it from the provided example file before running the app.

**Create your `.env` file by running this command from the main project folder:**

```
copy .env.example .env
```

This copies the example settings file into a new file called `.env` that the application will actually read.

**You can open `.env` with Notepad to view or edit it:**

```
notepad .env
```

### Environment Variables Explained

| Variable | Required? | Default Value | What It Does |
|---|---|---|---|
| `DEFAULT_DURATION_SECONDS` | Optional | `30` | Sets how many seconds the timer counts down from when you first open the app. Change this if you want a different starting duration (e.g., `60` for one minute). |
| `CORS_ORIGINS` | Optional | `http://localhost:5173,http://localhost:3000` | Tells the backend which browser addresses are allowed to communicate with it. The defaults cover the standard local development addresses and do not need to be changed for normal use. |

**Example `.env` file contents:**

```
DEFAULT_DURATION_SECONDS=30
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## 5. Run

The easiest way to start BLUEPRINT is to use the included boot script, which starts both the backend and frontend automatically.

**From the main project folder, run:**

```
boot.bat
```

Simply double-click `boot.bat` in File Explorer, **or** type the command above in Command Prompt while in the project folder.

The script will:
1. Start the FastAPI backend server
2. Start the React frontend

Once both are running, open your web browser and go to:

```
http://localhost:5173
```

You should see the BLUEPRINT retro timer application.

> **If you prefer to start the frontend manually** (for example, if the boot script only starts the backend), navigate to the `web` folder and run:
> ```
> cd web
> npm run dev
> ```

---

## 6. Stop

To shut down the application gracefully:

1. Click on the Command Prompt window where BLUEPRINT is running.
2. Press **Ctrl + C** on your keyboard.
3. If prompted with `Terminate batch job (Y/N)?`, type `Y` and press **Enter**.

If you opened two separate Command Prompt windows (one for backend, one for frontend), repeat these steps in each window.

You can now safely close the Command Prompt windows.

---

## 7. Key Settings Explained

| Setting | Where to Change It | Plain-Language Explanation |
|---|---|---|
| `DEFAULT_DURATION_SECONDS` | `.env` file | This is the number of seconds shown on the timer when the page first loads. Set it to `60` for a 1-minute default, `120` for 2 minutes, and so on. |
| `CORS_ORIGINS` | `.env` file | This is a security setting that controls which web addresses can talk to the timer's backend. Unless you are running the app on a different port or a different computer, you do not need to change this. |
| Frontend port (`5173`) | `web/package.json` or Vite config | The port number your browser uses to reach the app. `5173` is the default for the Vite development server used here. Only change this if something else on your computer is already using that port. |

---

## 8. Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python is not installed or not added to your system PATH | Re-install Python from https://www.python.org/downloads/ and **check the box that says "Add Python to PATH"** during installation |
| `'npm' is not recognized as an internal or external command` | Node.js is not installed or not added to your system PATH | Re-install Node.js from https://nodejs.org and restart Command Prompt after installation |
| Browser shows "This site can't be reached" at `localhost:5173` | The frontend server is not running | Make sure you ran `boot.bat` or `npm run dev` inside the `web` folder, and that no error messages appeared in Command Prompt |
| Backend error: `address already in use` | Another program (or a previous run of BLUEPRINT) is already using the backend port | Open Task Manager, find any running Python processes, end them, then try starting the app again |
| Timer face or colours do not appear correctly | Browser cache is showing an old version | Press **Ctrl + Shift + R** in your browser to do a hard refresh and clear the cache |
| `ModuleNotFoundError` when starting the backend | Python dependencies were not installed | Make sure you ran `pip install -r requirements.txt` from the main project folder (not the `web` folder) |