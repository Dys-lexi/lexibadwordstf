# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app
# Install system dependencies for font rendering
# RUN apt-get update && apt-get install -y \
#     libfreetype6-dev \
#     libfontconfig1-dev \
#     fontconfig \
#     fonts-dejavu \
#     && rm -rf /var/lib/apt/lists/*

# Copy bot code
COPY . .


# Install dependencies
RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r ./requiremrewnts.txt

# Set environment variable for virtual environment
ENV PATH="/venv/bin:$PATH"

ENV PYTHONUNBUFFERED=1


EXPOSE 3440

# Command to run the bot
CMD ["gunicorn", "--worker-class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker", "-w", "1","--bind", "0.0.0.0:3440", "search:app"]
# CMD ["python3", "search.py"]