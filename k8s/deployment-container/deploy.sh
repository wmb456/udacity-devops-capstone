#!/bin/bash

cat > deployment.yml
echo "--- deployment.yml created (sha256hash: $(sha256sum deployment.yml))"

if [ -z "${AWS_ACCESS_KEY_ID}" ] ; then
        echo "XXX missing env var AWS_ACCESS_KEY_ID. abort."
        exit 1
fi

if [ -z "${AWS_SECRET_ACCESS_KEY}" ] ; then
        echo "XXX missing env var AWS_SECRET_ACCESS_KEY. abort."
        exit 1
fi

if [ -z "${AWS_DEFAULT_REGION}" ] ; then
        echo "XXX missing env var AWS_DEFAULT_REGION. abort."
        exit 1
fi

if [ -z "${EKS_CLUSTER_NAME}" ] ; then
        echo "XXX missing env var EKS_CLUSTER_NAME. abort."
        exit 1
fi

echo "--- enable AWS access for kubectl"
aws eks --region ${AWS_DEFAULT_REGION} update-kubeconfig --name ${EKS_CLUSTER_NAME}

echo "--- run deployment"
kubectl apply -f ./deployment.yml
