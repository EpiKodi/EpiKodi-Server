web: gunicorn --worker-class socketio.sgunicorn.GeventSocketIOWorker app:app
release: python manage.py db upgrade