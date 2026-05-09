#!/bin/bash
# MONO-BOT-HUB Absolute Fixer

# 1. Create the necessary directory tree
mkdir -p lib configs scripts .github/workflows

# 2. Rename and move the hidden GitHub client
if [ -f ".github_app_client.py" ]; then
    mv .github_app_client.py lib/github_app_client.py
    echo "📦 Fixed: Moved .github_app_client.py to lib/github_app_client.py"
fi

# 3. Move scripts into the scripts folder
for f in monitor.py recovery.py global_royalty_audit.py emergency_halt.py rotate_keys.py; do
    if [ -f "$f" ]; then
        mv "$f" scripts/
        echo "✅ Moved $f to scripts/"
    fi
done

# 4. Create Python Package markers (Crucial for GitHub Actions)
touch lib/__init__.py
touch scripts/__init__.py

# 5. Initialize config manifest if missing
if [ ! -f "configs/fleet_manifest.json" ]; then
    echo "[]" > configs/fleet_manifest.json
fi

chmod +x setup_fleet.sh scripts/*.py
echo "🚀 Everything is now in the right place."
