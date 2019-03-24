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

## Step by step guide in deploying the application

1. Ensure you successfully have minikube and kubectl running on your workstation if you want to run locally 
2. Ensure you have a kubernetes cluster running and kubectl is installed if you want to run it in the cloud 
3. Do a git clone of the project
4. Have a copy of minikube running and all necessary things are setup
5. Navigate to the cloned project 
6. Change directory to kubernetes folder 
7. Run `kubectl apply -f mongodb-volume.yaml`, `kubectl apply -f mongodb-volume-claim.yaml`, `kubectl apply -f mongodb-deployment.yaml`, `kubectl apply -f api-deployment.yaml` this creates the deployment and service for the rest api and mongodb.
8. kubectl apply -f mongodb-volume-claim.yaml and mongodb-volume.yaml will make mongodb use persistent volume. mongodb-deployment.yaml will deploy monogodb on kubernetes 
9. api-deployment.yaml will deploy the rest api for this service
10. `kubectl apply -f mongodb-deployment.yaml` this creates the deployment and service for the mongodb
11. Pls note mongodb needs to come up first. i.e the pod and mongodb instance needs to be running and it should read 1/1. Once it comes up, then continue with the steps
12. `kubectl apply -f api-deployment.yaml` this creates the deployment and service for the rest api  
13. Run  `minikube service api --url` so you can get the ip address of the endpoint to call.
14. You can now test the endpoint http://minikubeip:port/<url of the endpoint below>

The following endpoints were implemented:

| Name                       | Method   | URL
| ---                        | ---      | ---
| Create user                | `POST`   | `/v1/register`
| Get the next integer       | `GET`    | `/v1/next?token=<generated_token>`
| Get the current integer    | `GET`    | `/v1/current?token=<generated_token>`
| Update the current integer | `PUT`    | `/v1/current?token=<generated_token>`
| Check health endpoint      | `GET`    | `/health`

Pls replace `generated_token` with the generated token once you do send post request to  `/v1/register` end point 

## Stack includes 

1. Flask framework 
2. MongoDB 
3. Nosetests tests
4. Docker 
5. Docker Compose
6. Kubernetes 