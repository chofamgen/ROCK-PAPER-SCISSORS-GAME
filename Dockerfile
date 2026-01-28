# 1. Base Image
FROM python:3.9-slim

# 2. Set directory
WORKDIR /app

# 3. Copy requirements
COPY requirements.txt .

# 4. Install dependencies (UPDATED SECTION)
# --upgrade pip: Updates the installer to the latest version (handles connection drops better)
# --default-timeout=1000: Tells pip to wait 1000 seconds before quitting (default is 15s)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=1000 -r requirements.txt

# 5. Copy code
COPY . .

# 6. Expose port
EXPOSE 8501

# 7. Run command
CMD ["streamlit", "run", "game_app.py", "--server.port=8501", "--server.address=0.0.0.0"]