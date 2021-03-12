#!/bin/bash

docker login --username ttannhaeuser

docker tag aws-k8s-deploy:0.0.1 ttannhaeuser/aws-k8s-deploy:0.0.1
docker tag aws-k8s-deploy:0.0.1 ttannhaeuser/aws-k8s-deploy:latest

docker push ttannhaeuser/aws-k8s-deploy