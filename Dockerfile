FROM python:3.11.1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic 
 



