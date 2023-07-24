# Use the official Python base image with Python 3.9
FROM python:3.9

# Set the working directory within the container
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Specify the command to run your Python application
CMD ["python", "jose.py"]
