import os
import shutil
from pathlib import Path
from typing import Optional

from .config import BACKUP_DIR


def create_backup(db_path: str | Path, backup_dir: str | Path = BACKUP_DIR) -> str:
    backup_path = Path(backup_dir)
    backup_path.mkdir(parents=True, exist_ok=True)
    db_file = Path(db_path)
    if not db_file.exists():
        raise FileNotFoundError(f"الملف غير موجود: {db_file}")
    filename = f"wallet_backup_{db_file.stem}_{backup_path.name}.sqlite3"
    target = backup_path / filename
    shutil.copy2(str(db_file), str(target))
    return str(target)


def restore_backup(db_path: str | Path, backup_file: str | Path) -> None:
    src = Path(backup_file)
    target = Path(db_path)
    if not src.exists():
        raise FileNotFoundError(f"ملف النسخ الاحتياطي غير موجود: {src}")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(target))
