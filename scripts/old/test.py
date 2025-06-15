import sys
import os
from pathlib import Path

# Force le chemin racine pour que `scripts/` soit accessible
racine = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(racine))

from scripts.db import connect_db

print(connect_db())
