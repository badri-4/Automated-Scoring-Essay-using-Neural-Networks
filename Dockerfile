# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Streamlit
RUN pip install streamlit

# Expose port 80
EXPOSE 80

# Run FastAPI and Streamlit apps
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run streamlit_app.py --server.port 80 --server.address 0.0.0.0"]
