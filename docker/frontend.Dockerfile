FROM python:3.11-slim

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY frontend ./frontend

CMD ["python", "-m", "frontend.app.main"]
