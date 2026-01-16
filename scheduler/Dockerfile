# Use official Python slim image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Ensure .local/bin is in PATH (for pip installed scripts like alembic)
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose ports for API and Streamlit
EXPOSE 8000 8501
