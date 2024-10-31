FROM python:3.9-slim

WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directory for tenant token storage
RUN mkdir -p storage

# Environment variables
ENV FLASK_APP=apiPacking.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 3000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]