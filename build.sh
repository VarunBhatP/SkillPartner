#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create superuser and add skills
python manage.py create_superuser
python manage.py add_skills

chmod +x build.sh