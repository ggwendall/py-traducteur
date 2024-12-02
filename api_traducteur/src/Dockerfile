# Use the official Python image as the base image
FROM python:3.10-slim

# Set environment variables to avoid interactive prompts during build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt /app/

# Install the dependencies with pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that the FastAPI application will run on
EXPOSE 8080

# Run the application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "debug"]