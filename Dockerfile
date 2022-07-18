FROM python:3.6-slim
ENV PYTHONUNBUFFERED 1

RUN mkdir /django_celery_proj
ADD . /django_celery_proj
WORKDIR /django_celery_proj
RUN pip install -r requirements.txt
EXPOSE 8000
CMD python manage.py runserver 0:8000