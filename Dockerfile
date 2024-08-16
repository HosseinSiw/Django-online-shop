FROM python:3.10

ENV PYTHONDONTWRITEBYCODE = 1
ENV PYTHONUNBUFFERED = 1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7000
CMD ["python", "manage.py", "runserver", "0.0.0.0:7000"]