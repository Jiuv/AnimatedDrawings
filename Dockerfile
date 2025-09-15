# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port available to the world outside this container
EXPOSE 8080

# Use Gunicorn to run the application. This is the production-standard way.
# It will run the 'app' object from the 'examples/fix_annotations.py' file.
# Cloud Run automatically provides the $PORT variable.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "examples.fix_annotations:app"]