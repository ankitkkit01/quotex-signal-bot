# Use Python 3.10 Slim Image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install git and other essential tools
RUN apt-get update && apt-get install -y git

# Upgrade pip and install requirements
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Run the bot
CMD ["python", "bot.py"]
