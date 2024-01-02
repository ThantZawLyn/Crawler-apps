 # Create Dockerfile.app
#Use your custom base image as the base image

FROM mglue/youtube-crawler-base-image:1.0

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
1) $ docker build -t youtube-comment-crawler-app:1.0 -f Dockerfile.app .
2) $ docker login
3) $ docker tag youtube-comment-crawler-app:1.0 mglue/youtube-comment-crawler-app:1.0
4) $ docker push mglue/youtube-comment-crawler-app:1.0
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
