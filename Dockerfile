FROM python:3.8-slim

WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files and folders to the container
COPY . .

# Expose port 8501 for Streamlit 
EXPOSE 8501

# Set the environment variable to avoid issues with Tkinter in Docker
ENV DISPLAY=:99

# Command to run the application
CMD ["python", "main.py"]
