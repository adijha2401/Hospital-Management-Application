Backend (Flask) for Hospital Management System (HMS)
====================================================

Quick start (local dev)
-----------------------

1. Create and activate a Python virtual environment:
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate

2. Install dependencies:
   pip install -r requirements.txt

3. Start Redis (required for caching & celery):
   redis-server

4. Run Flask app:
   python run.py
   The app will create `hms.db` and a default admin user (username=admin, password=Admin@123).

5. Run celery worker (in separate terminal):
   celery -A tasks.celery_app.celery worker --loglevel=info

6. Run celery beat (for periodic jobs):
   celery -A tasks.celery_app.celery beat --loglevel=info

Notes
-----
- Admin is created programmatically on first run (see `app/seeds/create_admin.py`). Change default password for production.
- The app uses SQLite file `hms.db` under backend/ by default.
- Replace `send_email` configuration in `app/utils/notifications.py` with proper SMTP settings or a mail service.
- The provided code is intentionally minimal to be easy to read and extend.

Directory layout
----------------
See the project architecture for how the backend files are organized.
