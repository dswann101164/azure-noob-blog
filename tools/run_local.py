# tools/run_local.py
import os, sys, traceback
from pathlib import Path

# Ensure imports work no matter where we're called from
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
os.chdir(PROJECT_ROOT)                 # run as if from project root
sys.path.insert(0, str(PROJECT_ROOT))  # allow "import app"

from app import app

SITE_URL = os.environ.get("SITE_URL") or "http://127.0.0.1:5050"
HOST = "127.0.0.1"
PORT = 5050

print(f"SITE_URL={SITE_URL}", flush=True)
print(f"Starting Flask on http://{HOST}:{PORT} (no reloader)...", flush=True)

try:
    app.run(debug=True, host=HOST, port=PORT, use_reloader=False)
except Exception as e:
    print("Flask failed to start:", e, file=sys.stderr, flush=True)
    traceback.print_exc()
    sys.exit(1)
