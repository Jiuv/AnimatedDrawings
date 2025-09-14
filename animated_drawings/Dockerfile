# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container at /app
COPY . .

# Make port 5050 available to the world outside this container
EXPOSE 5050

# Define environment variable
ENV NAME World

# Run fix_annotations.py when the container launches
# We've modified the command to work on the server
CMD ["python", "examples/fix_annotations.py", "examples/drawings"]