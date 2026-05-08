#!/bin/bash

echo "🚀 Initializing Mono-Bot-Hub Architecture..."

# Create Directory Structure
mkdir -p .github/workflows
mkdir -p core-engine/providers
mkdir -p configurations
mkdir -p manager
mkdir -p scripts
mkdir -p lib
mkdir -p secrets

# Create Placeholder Files
touch configurations/fleet-manifest.csv
touch secrets/app-private-key.pem
touch .env

# Set Permissions
chmod +x manager/deployer.py
chmod +x scripts/emergency_halt.py

echo "✅ Structure Created. Please add your GitHub App Private Key to /secrets."
