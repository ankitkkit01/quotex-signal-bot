# ✅ Use Python 3.10 Slim Image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy all project files into container
COPY . /app

# Upgrade pip & install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Run the bot
CMD ["python", "bot.py"]
