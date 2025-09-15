# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Use Gunicorn to run the application on the correct port.
# Cloud Run provides the $PORT environment variable, which will be 8080.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "examples.fix_annotations:app"]