import json
import os
from datetime import datetime

LOG_FILE = "user_logs.json"

def log_user_data(data):
    # Ajoute un timestamp automatiquement
    data["timestamp"] = datetime.utcnow().isoformat()

    # Crée le fichier s'il n'existe pas
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    # Lit les logs existants
    with open(LOG_FILE, "r") as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            logs = []

    # Ajoute la nouvelle entrée
    logs.append(data)

    # Sauvegarde les logs
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)
