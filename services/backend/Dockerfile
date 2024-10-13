FROM python:3.11-slim

WORKDIR /app

COPY services/backend/src/ .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]