FROM python:3.10-slim

# Install git (very important for quotexpy)
RUN apt-get update && apt-get install -y git

# Set working directory
WORKDIR /app

# Copy all files into container
COPY . /app

# Install pip requirements
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# Run the bot
CMD ["python", "bot.py"]
