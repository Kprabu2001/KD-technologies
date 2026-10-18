#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install project dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --no-input
