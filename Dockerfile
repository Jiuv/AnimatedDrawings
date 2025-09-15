# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire project into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Use Gunicorn to run the application in a production-ready way
# It will look inside the 'examples/fix_annotations.py' file for a variable named 'app'
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--workers", "1", "examples.fix_annotations:app"]