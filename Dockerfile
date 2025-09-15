# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the entire project into the /app directory
COPY . .

# Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Tell the world that the container listens on port 8080
EXPOSE 8080

# This is the industry-standard way to run a Flask app with Gunicorn.
# It tells Gunicorn to run the 'app' object from the 'examples.fix_annotations' module.
CMD ["gunicorn", "--bind", "0.
0.0.0:8080", "examples.fix_annotations:app"]