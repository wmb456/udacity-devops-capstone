#! /bin/bash 

echo "-------------------------------"
date -Is
echo "-------------------------------"

echo
kubectl get pods -o wide

kubectl get pods -o=jsonpath='{range .items[*]}{"\n"}{.metadata.name}{":\t"}{range .spec.containers[*]}{.image}{", "}{end}{end}' 

echo
echo
kubectl rollout status deployment cowsay-web-rolling-update

echo
kubectl get deployment cowsay-web-rolling-update
