# TechSalo
Django-Cron Job

1)- Install python3, rabbitmq and start its server with default settings and create a folder

2)- Inside folder create and activate virtual Env
  python3 -m venv venv
  source venv/bin/activate

3)- clone the repo and install dependencies
  cd TechSalo
  pip install --upgrade pip
  pip install -r requirements.txt

4)- Migrate db changes
  python manage.py makemigrations
  python manage.py migrate

5)- start server, celery worker, celery beat
  python manage.py runserver
  celery -A main beat -l debug
  celery -A main worker -l debug

Cron job named send_notification will start running every minute that can be modified from crontab
