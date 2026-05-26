import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# =========================
# DATA
# =========================

DATA_DIR = PROJECT_ROOT / "data"

DATA_RAW = DATA_DIR / "raw"
DATA_INTERIM = DATA_DIR / "interim"
DATA_PROCESSED = DATA_DIR / "processed"


# =========================
# REPORTS
# =========================

REPORTS_DIR = PROJECT_ROOT / "reports"

FIGURES_DIR = REPORTS_DIR / "figures"
TABLES_DIR = REPORTS_DIR / "tables"
MAPS_DIR = REPORTS_DIR / "maps"


# =========================
# CREATE DIRECTORIES
# =========================

DIRECTORIES = [
    DATA_RAW,
    DATA_INTERIM,
    DATA_PROCESSED,
    FIGURES_DIR,
    TABLES_DIR,
    MAPS_DIR,
]

for directory in DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)