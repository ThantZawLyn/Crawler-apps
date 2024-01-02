# Use your custom base image as the base image
FROM mglue/youtube-base-image:1.0

# Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt .

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python project files into the container
COPY app.py .

# Run the NLP application
CMD ["python", "app.py"]