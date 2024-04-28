# Use the official Python image as a base
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY src/ .

# Expose the port that the Flask app runs on
EXPOSE 8000

# Command to run the Flask app
CMD ["python", "-u", "server.py"]

# docker run -p 8000:8000 -e API_KEY=xyz weather-app

# Environment variables:
# - API_KEY:  openweathermap API key, mandatory