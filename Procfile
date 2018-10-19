release: python manage.py migrate
web: gunicorn knoteserver.wsgi:application --log-file -
