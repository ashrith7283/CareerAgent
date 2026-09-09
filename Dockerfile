FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Render sets PORT env var; Gradio defaults to 7860 if not set
EXPOSE 10000

# Run the app
CMD ["python", "app.py"]
