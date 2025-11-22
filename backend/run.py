"""
Entry point to run the Flask app locally.
Usage:
    export FLASK_APP=run.py
    python run.py
"""
from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Use 0.0.0.0 for external local access, port 5000 by default
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
