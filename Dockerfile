FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV GROQ_API_KEY=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

EXPOSE 5000

CMD ["flask", "run"]
