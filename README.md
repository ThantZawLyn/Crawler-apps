# Create Dockerfile.base for all-content base image.

#Use an official Python runtime as a parent image
FROM joyzoursky/python-chromedriver:3.8-selenium

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt .

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy your Python project files into the container
COPY app.py .

#Define the command to run your Python application
CMD ["python", "app.py"]
================================================
# Docker build command line
1) $docker build -t all-content-base-image:1.1 -f Dockerfile.base .
2) $ docker login
3) $ docker tag all-content-base-image:1.1 mglue/all-content-base-image:1.1
4) $ docker push mglue/all-content-base-image:1.1
============================================  
# Create Dockerfile.app for all-content app.

# Use your custom base image as the base image
FROM mglue/all-content-base-image:1.1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
#COPY keyword.txt .

# Copy the requirements.txt file into the container
#COPY stopword.txt .

# Copy your Python project files into the container
COPY . /app

# Run the NLP application
CMD ["python", "app.py"]
============================
# Command line
1) $ docker build -t all-content-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag all-content-app:1.1 mglue/all-content-app:1.1
4) $ docker push mglue/all-content-app:1.1
5) 
# Push Code to GitHub
1) git add . 
2) git commit -m "Initial commit"
3) git remote add origin https://github.com/ThantZawLyn/Yae-Naung-App.git
4) git branch -M main
5) git push -u origin main
# Set Up GitHub Actions for Continuous Integration (CI)
Create a .github/workflows/docker.yml file in GitHub repository 
# Set Up Docker Hub and Push Docker Image
docker login -u username -p yourpassword
# Deploy Application on Kubernetes
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create Dockerfile.app "Fb-nlp"app.
# Use your custom base image as the base image
FROM mglue/all-content-base-image:1.1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
#COPY keyword.txt .

# Copy the requirements.txt file into the container
#COPY stopword.txt .

# Copy your Python project files into the container
COPY . /app

# Run the NLP application
CMD ["python", "app.py"]
===================================================
# Command line
1) $ docker build -t fb-nlp-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag fb-nlp-app:1.0 mglue/fb-nlp-app:1.0
4) $ docker push mglue/fb-nlp-app:1.0
5) 
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create Dockerfile.base

#Use an official Python runtime as a parent image
FROM joyzoursky/python-chromedriver:3.8-selenium

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt .

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy your Python project files into the container
COPY app.py .

#Define the command to run your Python application
CMD ["python", "app.py"]

# Docker build command line
1) $ docker build -t telegram-base-image:1.0 -f Dockerfile.base .
2) $ docker login
3) $ docker tag telegram-base-image:1.0 mglue/telegram-base-image:1.0
4) $ docker push mglue/telegram-base-image:1.0
   
# Create Dockerfile.app
#Use your custom base image as the base image
FROM mglue/telegram-base-image:1.0

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
#COPY keyword.txt .

#Copy the requirements.txt file into the container
#COPY stopword.txt .

#Copy your Python project files into the container
COPY app.py .

#Run the NLP application
CMD ["python", "app.py"]

# Command line
1) $ docker build -t telegram-crawler-app:1.1 -f Dockerfile.app .
2) $ docker login
3) $ docker tag telegram-crawler-app:1.1 mglue/telegram-crawler-app:1.1
4) $ docker push mglue/telegram-crawler-app:1.1
5) 
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create Dockerfile.base

#Use an official Python runtime as a parent image
FROM joyzoursky/python-chromedriver:3.8-selenium

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
COPY requirements.txt .

#Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Copy your Python project files into the container
COPY app.py .

#Define the command to run your Python application
CMD ["python", "app.py"]

# Docker build command line
1) $ docker build -t youtube-base-image:1.0 -f Dockerfile.base .
2) $ docker login
3) $ docker tag youtube-base-image:1.0 mglue/youtube-base-image:1.0
4) $ docker push mglue/youtube-base-image:1.0
   

++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Use your custom base image as the base image
FROM mglue/youtube-base-image:1.0

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
#COPY keyword.txt .

# Copy the requirements.txt file into the container
#COPY stopword.txt .

# Copy your Python project files into the container
COPY app.py .

# Run the NLP application
CMD ["python", "app.py"]
======================================================
# Command line
1) $ docker build -t yt-comment-analysis-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag yt-comment-analysis-app:1.0 mglue/yt-comment-analysis-app:1.0
4) $ docker push mglue/yt-comment-analysis-app:1.0
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
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
======================================================
# Command line
1) $ docker build -t yt-comment-crawler-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag yt-comment-crawler-app:1.0 mglue/yt-comment-crawler-app:1.0
4) $ docker push mglue/yt-comment-crawler-app:1.0
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Use your custom base image as the base image
FROM mglue/youtube-base-image:1.0

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
#COPY keyword.txt .

# Copy the requirements.txt file into the container
#COPY stopword.txt .

# Copy your Python project files into the container
COPY app.py .

# Run the NLP application
CMD ["python", "app.py"]
======================================================
# Command line
1) $ docker build -t yt-channel-crawler-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag yt-channel-crawler-app:1.0 mglue/yt-channel-crawler-app:1.0
4) $ docker push mglue/yt-channel-crawler-app:1.0
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create Dockerfile.app
#Use your custom base image as the base image
FROM mglue/youtube-base-image:1.0

#Set the working directory in the container
WORKDIR /app

#Copy the requirements file into the container
#COPY keyword.txt .

#Copy the requirements.txt file into the container
#COPY stopword.txt .

#Copy your Python project files into the container
COPY app.py .

#Run the NLP application
CMD ["python", "app.py"]
======================================================================================
# Command line
1) $ docker build -t yt-update-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag yt-update-app:1.0 mglue/yt-update-app:1.0
4) $ docker push mglue/yt-update-app:1.0
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Use your custom base image as the base image
FROM mglue/youtube-base-image:1.0

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
#COPY keyword.txt .

# Copy the requirements.txt file into the container
#COPY stopword.txt .

# Copy your Python project files into the container
COPY app.py .

# Run the NLP application
CMD ["python", "app.py"]
======================================================
# Command line
1) $ docker build -t yt-video-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag yt-video-app:1.0 mglue/yt-video-app:1.0
4) $ docker push mglue/yt-video-app:1.0
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++