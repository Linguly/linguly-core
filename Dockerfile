# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Set the environment variables
ARG BASIC_MODEL_URL
ENV BASIC_MODEL_URL=$BASIC_MODEL_URL

ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

# Expose the port the app runs on
EXPOSE 3001

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3001"]