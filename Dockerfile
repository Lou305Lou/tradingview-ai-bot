FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy all project files into /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]
