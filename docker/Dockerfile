FROM python:3.12.3-slim
COPY ../app /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
LABEL Version="0.1"
CMD ["python", "app.py"]
