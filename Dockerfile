# ✅ Use Python 3.10 (not 3.9)
FROM python:3.10-slim

# 🛠️ Install git (IMPORTANT)
RUN apt-get update && apt-get install -y git

# 📁 Set working directory
WORKDIR /app

# 📂 Copy all project files to /app
COPY . /app

# 🧪 Upgrade pip + install requirements
RUN pip install --no-cache-dir --upgrade pip
RUN if [ -f "requirements.txt" ]; then pip install --no-cache-dir -r requirements.txt; fi

# ▶️ Run the bot
CMD ["python", "bot.py"]
