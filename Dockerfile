# 1. Base Image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy requirements first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
# We use --no-cache-dir to keep the image small
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your code
COPY . .

# 6. Expose the port Streamlit uses
EXPOSE 8501

# 7. The command to run the app
CMD ["streamlit", "run", "game_app.py", "--server.port=8501", "--server.address=0.0.0.0"]