# Dockerized web application built with Django, with a container orchestration system.

* This is a cloud-based Web Application built as a part of my Cloud Computing course (Jan 2019).  
* The project is REST API based photo sharing platform built using Django. The application has been Dockerized.  
* The app was split into 2 microservices and run on Docker containers hosted on separate AWS EC2 instances.  
* I built a container orchestrator that does auto-scaling and load balancing.  
* The work based on the number (and type) of requests that the servers (containers) receive.  
* The count of servers (containers) is increased if the total load is high. Vice-versa, the containers are downscaled if the load is low.  
