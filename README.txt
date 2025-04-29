Name:
NetID:

Challenges Attempted (Tier I/II/III): None
Working Endpoint: GET /api/courses/
Your Docker Hub Repository Link: https://hub.docker.com/u/mukeku

Questions:
Explain the concept of containerization in your own words.
Containerization is the process of packaging an application and everything it needs — code, libraries, settings — into a lightweight, portable unit called a container. This ensures the app runs consistently across different environments, solving the "it works on my machine" problem. Tools like Docker make it easy to build, ship, and run containers anywhere.

What is the difference between a Docker image and a Docker container?
A Docker image is a blueprint — it’s a snapshot of everything needed to run an application, including the code, libraries, and environment settings. A Docker container is a running instance of that image, like a live, isolated application. You can create many containers from the same image.

What is the command to list all Docker images?
docker images

What is the command to list all Docker containers?
docker ps -a

What is a Docker tag and what is it used for?
A Docker tag is a label used to identify different versions of a Docker image. It helps you manage, pull, and push specific versions of an image easily.

What is Docker Hub and what is it used for?
Docker Hub is an online repository where developers can store, share, and distribute Docker images publicly or privately.

What is Docker compose used for?
Docker Compose is used to define and run multi-container Docker applications by using a docker-compose.yml file to configure services, networks, and volumes in one place.

What is the difference between the RUN and CMD commands?
RUN executes commands at build time to create the image (like installing libraries), while CMD specifies the default command to run when a container starts.