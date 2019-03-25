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
| Register  user             | `POST`   | `/v1/register`
| Get the next integer       | `GET`    | `/v1/next?token=<generated_token>`
| Get the current integer    | `GET`    | `/v1/current?token=<generated_token>`
| Update the current integer | `PUT`    | `/v1/current?token=<generated_token>`
| Check health endpoint      | `GET`    | `/health`

Pls replace `generated_token` with the generated token once you do send post request to  `/v1/register` end point 

`output_images` folder contains screenshot of the test i need to confirm that all the end points are working fine. This test was done using `postman`

## Stack includes 

1. Flask framework 
2. MongoDB 
3. Nosetests tests
4. Docker 
5. Docker Compose
6. Kubernetes 
7. Github

## Questions and answers
Questions 1 to 4 can be found under endpoints that were implemented session
5. Deploy your application to the cloud and either show or tell us how you might monitor it. 
Answer: The application was deployed on kubernetes which have an health endpoint. This endpoint checks mongodb and if there is a bug in the code.. The health endpoint will not come up if there is an error . In monitoring the application, i will make use of the following tools : 
1. Nagios 
2. Monitis which will check the application from different regios of the world 
3. Promethus 
4. Will also implement pagerduty, which will call the engineer on call if the health endpoint is not up 

6. Explain how you would go about making sure that the application is highly  available.This would include the application itself as well as any other  services that is uses (like a database
Answer: The application was deployed on kubernetes and kubernetes supports running multiple instances of the application, in kubernetes it is called `replicas`. Presently two instance of the application are running, however more than 2 instances can be configured to run and if the application goes down other instance can pickup which will prevent the downtime. For the database i use mongodb in this exercrise, mongodb supports high availability which is having a replicaset of serveral mongodb instance running and 1 of the instance will be the primary database and the others will be readonly. Since the application and database support high avaliablity this will promote business continuity.  


## Stretch Goals (if you feel like showing off a bit)    
1. Hook up APM using a service like ​https://www.elastic.co/
Answer: I planned to integrate datadog to the rest endpoint. I will have to follow this tutorial for kubernetes in achiveing this https://www.datadoghq.com/blog/monitor-kubernetes-docker/
I have worked appDynamic in the past. 
   
2. Allow sign up using OAuth  a. Github, Facebook, Google, anything that supports it!
Answer: I used JSON Web Token Authentication for the signup and i discussed this with the hiring manager