web: gunicorn --config gunicorn.conf.py --chdir app site_settings.wsgi
release: app/manage.py migrate --no-input