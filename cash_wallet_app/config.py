from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "cash_wallet.db"
BACKUP_DIR = DATA_DIR / "backups"
APP_NAME = "نظام محفظة النقدية"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "Admin123!"
SESSION_TIMEOUT_MINUTES = 30
ALLOW_NEGATIVE_BALANCES = False

DATA_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)
