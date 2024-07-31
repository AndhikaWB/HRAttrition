# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory in the container
# Will affect other instructions such as COPY, RUN, CMD, etc
# The directory will be created if not exist
WORKDIR /app

# Copy the requirements.txt file to the container
COPY ./requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files to the container
# If source is a dir, it will copy everything but the dir itself
COPY ./model ./model
COPY ./data ./data
COPY ./*.py .

# Expose the port that the application will run on
EXPOSE 8000

# Command to run the application when the container starts
# When running inside Docker, use 0.0.0.0 as host, 127.0.0.1 otherwise
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]