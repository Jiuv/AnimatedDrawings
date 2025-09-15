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

# --- THE FINAL FIX ---
# Tell Gunicorn to change into the 'examples' directory before starting.
# Then, tell it to run the 'app' from the 'fix_annotations' file.
CMD ["gunicorn", "--bind", "0.0.0.0:5050", "--chdir", "examples", "fix_annotations:app"]