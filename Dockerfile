FROM python:3.11-slim

WORKDIR /app

# Copy code and data
COPY src/ ./src
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV GROQ_API_KEY=<YOUR_GROQ_API_KEY>

EXPOSE 5000

CMD ["flask", "run"]
