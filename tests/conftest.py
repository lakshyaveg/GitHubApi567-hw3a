
printf "" > src/__init__.py

cat <<'EOF' > tests/conftest.py
import os, sys
# Add the repo root to sys.path so "import src.gh_api" works
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
