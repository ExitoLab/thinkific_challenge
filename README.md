### Description

This application was developed with Python programming language using the Flask Framework. NoSQL database was implemented and MongoDB was considered as the database because of its flexibility. The application is dockerize and running on kubernetes. Both the rest api and the database (mongodb) are both running on kubernetes. The image for the application is already shipped to docker hub and can easily be access from there. 

I also prefer to do unit testing for all my codes, this is a standard i recently adopted. For the unit testing i decided to use Nosetests. Serveral test cases were carrying out.
The testcase can be found in test_endpoint.py

The folder `kubernetes` contains all the yaml files for running the application. The mongodb was deployed using persistent volume, this means that if the docker container go missing or deleted it will not affect the data. The data can be mounted on a different docker container. The service and deployment for the rest api and mongodb can in a single file respectively 

To run this application, the rest service needs to be deployed in a kubernetes environment. This can be deployed in the cloud and also locally. In deploying the app locally, it requires installing minikube and kubectl. Minikube is the standalone and lightweight kubernetes master and node while kubectl is an application running on kubernetes which will be used in deploying the application

### Description of the database

1. MongoDB was used for this project 
2. The name database for this project is `thinkific_challenge` 
3. There are two collections `incremental_counter` and `users`
4. The `incremental_counter` contains the record of the incremental id
5. The `users` contains details of the user that registered such as `email`, `hashed password`, `token`,    `incremental_id`.

## Stack includes 

1. Flask framework 
2. MongoDB 
3. Nosetests tests
4. Docker 
5. Docker Compose
6. Kubernetes 