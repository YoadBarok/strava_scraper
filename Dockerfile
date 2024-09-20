FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Expose port 8080 to the outside world
EXPOSE 8080

# Command to run the app with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "src.server:app"]

