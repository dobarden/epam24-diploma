# Diploma project EPAM Cloud&Devops Internship 24 stream.

A simple Python application on Flask framework with a MySQL database. Retrieves data about Star Wars universe from the https://swapi.dev/ using open API, stores and updates the data in the database, and displays the data.

## swapp

Includes app files

## terraform

Includes two folders with terraform manifests to deploy:
 - Kubernetes cluster in an AWS EKS with RDS MySQL databases,
 - EFS, EC2 instance and installs Jenkins and SonarQube on it.

## jenkins

Includes:
 - CI/CD pipelines and k8s manifests for deploying an app on a Kubernetes cluster, 
 - pipelines for deploying Prometheus+Grafana, ELK stack, Ingress controller, and a Cluster-autoscaler.