FROM python:3.10-slim

# Install ffmpeg and dependencies
RUN apt-get update && apt-get install -y ffmpeg git curl && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all files to working directory
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port
EXPOSE 7860

# Run the app
CMD ["python", "app.py"]
