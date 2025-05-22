FROM python:3.11-slim

# Install Tkinter and GUI libraries
RUN apt-get update && \
    apt-get install -y python3-tk tk-dev libx11-6 libxext6 libxrender1 libxtst6 libxi6 libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and input/output folders
COPY app/ /app/
COPY input/ /input/
COPY output/ /output/

CMD ["python", "main.py"]
