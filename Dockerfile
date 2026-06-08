# Use official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy the application code
COPY app/app.py .

# Expose the port the app runs on
EXPOSE 8080

# Run the application
CMD ["python", "app.py"]