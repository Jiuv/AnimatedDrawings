# Use an official Python runtime as a parent image
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "examples.fix_annotations:app"]