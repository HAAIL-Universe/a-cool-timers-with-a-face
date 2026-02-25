# User Instructions

---

## 1. Prerequisites

Before you begin, make sure the following software is installed on your Windows computer. Click each link to download.

| Software | Minimum Version | Download Link |
|---|---|---|
| Python | 3.9 or higher | https://www.python.org/downloads/ |
| Node.js (includes npm) | 18.0 or higher | https://nodejs.org/en/download |
| PostgreSQL | 13.0 or higher | https://www.postgresql.org/download/windows/ |

**How to check if these are already installed:**

Open Command Prompt (press `Windows Key + R`, type `cmd`, press Enter) and run:

```
python --version
node --version
npm --version
psql --version
```

Each command should print a version number. If you see an error instead, that program needs to be installed.

> **Tip during Python install:** On the first screen of the Python installer, check the box that says **"Add Python to PATH"** before clicking Install. This is required.

---

## 2. Install

These steps download all the code libraries the application needs. You only need to do this once.

**Step 1 — Install Python dependencies (the backend engine)**

Open Command Prompt, navigate to the main project folder, and run:

```
pip install -r requirements.txt
```

This installs FastAPI and all supporting Python packages.

**Step 2 — Install JavaScript dependencies (the visual frontend)**

Still in Command Prompt, navigate into the `web` subfolder:

```
cd web
npm install
```

This downloads everything the React/Vite visual interface needs. It may take a minute or two — this is normal.

After it finishes, go back to the main project folder:

```
cd ..
```

---

## 3. Credential / API Setup

**PostgreSQL Database Setup**

This application stores timer data in a PostgreSQL database. You need to create a database for it to use.

1. Open the **pgAdmin** application that was installed with PostgreSQL (look in your Start Menu).
2. Connect to your local PostgreSQL server (the password you set during PostgreSQL installation).
3. Right-click **Databases** → **Create** → **Database**.
4. Name it `timers_db` and click **Save**.

You will also need your PostgreSQL **username** and **password** (the ones you chose during installation — the default username is usually `postgres`).

No external API keys or third-party accounts are required.

---

## 4. Configure .env

The `.env` file is a simple text file that tells the application important settings — like how to connect to your database and how to keep things secure. Think of it as a personalised settings card.

**Create the file by running this command** from the main project folder in Command Prompt:

```
copy .env.example .env
```

> If no `.env.example` file exists, create a new file called `.env` in the main project folder using Notepad.

Open `.env` in Notepad (or any text editor) and fill it in using the guide below:

```
DATABASE_URL=postgresql://user:password@localhost:5432/timers_db
JWT_SECRET=your-secret-key-here-change-in-production
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
DEFAULT_DURATION_SECONDS=30
```

**What each setting means:**

| Variable | What It Does | Required? | What to Change |
|---|---|---|---|
| `DATABASE_URL` | The address and login details for your PostgreSQL database | Optional (has default) | Replace `user` with your PostgreSQL username and `password` with your PostgreSQL password. Example: `postgresql://postgres:mypassword@localhost:5432/timers_db` |
| `JWT_SECRET` | A secret password the app uses to secure user sessions. Think of it like a lock combination. | Optional (has default, **but change it!**) | Replace with any long random string of letters and numbers. Example: `xK9mP2qLr7nV4wZ1` |
| `CORS_ORIGINS` | Tells the backend which web addresses are allowed to talk to it | Optional | Leave as default unless you know you are running things on different ports |
| `DEFAULT_DURATION_SECONDS` | How many seconds a new timer starts with by default | Optional | Change `30` to any number of seconds you prefer (e.g., `60` for one minute) |

**Important:** Save the file after making your changes.

---

## 5. Run

Once installation and configuration are complete, starting the app is easy.

**Start everything with the boot script:**

In Command Prompt, make sure you are in the main project folder, then run:

```
boot.bat
```

This single command starts both the backend (FastAPI) and the frontend (React) together.

**Alternatively, start each part manually:**

*Backend (open a Command Prompt window and run):*
```
uvicorn main:app --reload
```

*Frontend (open a second Command Prompt window, go into the `web` folder, and run):*
```
cd web
npm run dev
```

**Once running, open your web browser and go to:**

```
http://localhost:3000
```

You should see the retro 8-bit timer interface.

> The backend API runs at `http://localhost:8000`. You don't need to open this directly — the frontend connects to it automatically.

---

## 6. Stop

**To stop the application:**

1. Click on the Command Prompt window that is running the app.
2. Press **Ctrl + C** on your keyboard at the same time.
3. You may see a message asking `Terminate batch job (Y/N)?` — type `Y` and press Enter.

If you started the backend and frontend in separate windows, repeat this step in each window.

It is safe to close the Command Prompt windows after stopping.

---

## 7. Key Settings Explained

Here is a plain-language explanation of the most important settings you might want to adjust:

**`DATABASE_URL`**
This is the "address" the app uses to find and log into your database. It follows the pattern:
`postgresql://[your-username]:[your-password]@localhost:5432/[database-name]`
If you named your database something other than `timers_db`, change that part here.

**`JWT_SECRET`**
This is a private key used to protect user login sessions. If someone were to guess it, they could potentially access the app without a valid login. **Always change the default value** before sharing or deploying this app. Make it long and random — something like `BluePrint_T1m3r_S3cur3_K3y_2024!`.

**`CORS_ORIGINS`**
CORS stands for "Cross-Origin Resource Sharing" — it is a browser security rule that controls which web addresses can communicate with the backend. If you run the frontend on a different port or a different computer, add that address here, separated by a comma.

**`DEFAULT_DURATION_SECONDS`**
This sets the starting countdown duration when you create a new timer. `30` means 30 seconds. Change it to `60` for one minute, `120` for two minutes, and so on.

---

## 8. Troubleshooting

| Problem / Error Message | Likely Cause | How to Fix |
|---|---|---|
| `'python' is not recognized as an internal or external command` | Python was not added to your system PATH during installation | Reinstall Python from python.org and **make sure to check "Add Python to PATH"** on the first screen |
| `'npm' is not recognized as an internal or external command` | Node.js is not installed or was installed incorrectly | Download and reinstall Node.js from nodejs.org, then restart Command Prompt |
| `connection to server at "localhost" failed` or database connection error | PostgreSQL is not running, or the credentials in `.env` are wrong | Open Windows Services (search "Services" in Start Menu), find **postgresql**, and click **Start**. Also double-check your username and password in the `DATABASE_URL` setting |
| `Address already in use` or `port 8000 already in use` | Another program (or a previous run of this app) is already using that port | Close any other Command Prompt windows running the app, or restart your computer |
| `Module not found` or `ModuleNotFoundError` | Python dependencies were not installed, or you are running from the wrong folder | Make sure you ran `pip install -r requirements.txt` from the **main project folder**, not from inside `web/` |
| The browser shows a blank page or "Cannot connect" | The frontend or backend has not fully started yet | Wait 10–15 seconds and refresh the page. If it still fails, check that both `boot.bat` ran without errors in Command Prompt |