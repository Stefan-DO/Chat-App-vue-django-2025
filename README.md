# Chat-App-Vue-Django-2025

This repository contains a simple real-time chat application built with Django (DRF + Djoser + Channels) for the backend and Vue 3 + Vite for the frontend.

## Quick start (backend)

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
& ".\.venv\Scripts\Activate.ps1"
```

2. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

3. Apply migrations and create a superuser if needed:

```powershell
cd chatire-backend
python manage.py migrate
python manage.py createsuperuser
```

4. Start the development server (choose one):

- Django dev server (simple):

```powershell
python manage.py runserver 0.0.0.0:8000
```

- Daphne (recommended for WebSockets in production-like environment):

```powershell
pip install daphne
daphne -b 0.0.0.0 -p 8000 chatire.asgi:application
```

Note: For multi-process/production WebSocket support, configure Redis and `CHANNEL_LAYERS`.

## Quick start (frontend)

1. Install Node.js dependencies:

```powershell
cd chatire-frontend
npm install
```

2. Start the dev server:

```powershell
npm run dev
```

3. Open the app in the browser (Vite usually runs at `http://localhost:5173`).

## Notes
- The backend exposes auth routes via Djoser at `/auth/` (signup: `POST /auth/users/`, login: `POST /auth/token/login/`).
- WebSocket path: `ws://localhost:8000/ws/chat/<uri>`.
- Environment variables and production settings are not included — avoid using `DEBUG=True` or the included secret key in production.

If you want, I can also add a `Makefile` or PowerShell script to automate these steps.
