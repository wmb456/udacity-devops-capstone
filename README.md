# udacity-devops-capstone

```
  _________________________________________________
 /                                                 \
| Udacity AWS DevOps capstone project bringing      |
| cowsays to the web :-)                            |
 \                                                 /
  =================================================
                                                      \
                                                       \
                                                         ^__^
                                                         (oo)\_______
                                                         (__)\       )\/\
                                                             ||----w |
                                                             ||     ||
```

# service API

... just as a bunch of curl calls...

## service version

```
curl -X GET http://127.0.0.1:8080/
```

## available speakers

```
curl -X GET http://127.0.0.1:8080/speakers
```

## say something as...

```
curl -X POST -F 'speaker=stimpy' -F 'message=Blargh!' http://127.0.0.1:8080/say
```

# development

## setup

The project requires python >= 3.6.

```
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

## liniting / testing

Run the linter:

```
pylint *.py
```

Run basic smoke test:
```
python smoke_test.py
```

**Note:** smoke tests accepts the target address (<host>:<port>) as env var _COWSAY_SERVICE_ADDRESS_

## pipeline eks-k8s deployment container

The container image _ttannhaeuser/aws-k8s-deploy:latest_ used in the pipeline is build using the files/scripts in the folder _k8s/deployment-container_.

The image expects an k8s deployment description (see _k8s/cowsay-deployment-template.yml) on stdin as well as a bunch of environment variables.

See _k8s/deployment-container/deploy.sh_ for more information.

# k8s environment

## dependencies

aws cli (1.19.5):
```
python3.9 -m venv .venv
. .venv/bin/activate
pip install awscli==1.19.5
```

install kubectl (1.18):
```
curl -o kubectl https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/linux/amd64/kubectl

sha256sum kubectl
3dbe69e6deb35fbd6fec95b13d20ac1527544867ae56e3dae17e8c4d638b25b9  kubectl

sudo mv kubectl /usr/local/bin
```

also see/other versions: https://docs.aws.amazon.com/eks/latest/userguide/install-kubectl.html

install eksctl (latest):
```
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp

sha256sum /tmp/eksctl
789dcb3b3562455e1f47d131fed8f656d618f4e73b1089ba3c7dba66b6435e3b  /tmp/eksctl

sudo mv /tmp/eksctl /usr/local/bin
eksctl version
```

also see: https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html

install 
```
curl https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/aws-iam-authenticator

sha256sum aws-iam-authenticator

fe958eff955bea1499015b45dc53392a33f737630efd841cd574559cc0f41800  aws-iam-authenticator

sudo mv aws-iam-authenticator /usr/local/bin
```

also see: https://docs.aws.amazon.com/eks/latest/userguide/install-aws-iam-authenticator.html

## prepare the cluster

1. prepare the environment
```
./setup-cluster.sh

2021-03-12 20:32:21 [ℹ]  eksctl version 0.40.0
2021-03-12 20:32:21 [ℹ]  using region eu-central-1
...
2021-03-12 20:50:08 [✔]  EKS cluster "udacity-capstone" in "eu-central-1" region is ready

kubectl get nodes
NAME                                              STATUS   ROLES    AGE    VERSION
ip-192-168-21-179.eu-central-1.compute.internal   Ready    <none>   97s    v1.18.9-eks-d1db3c
ip-192-168-57-141.eu-central-1.compute.internal   Ready    <none>   100s   v1.18.9-eks-d1db3c
```
2. enable access for kubectl on the newly created cluster (usually done by the cluster setup)
```
setup-kubectl.sh

Added new context arn:aws:eks:eu-central-1:xxxxxxxxx:cluster/udacity-capstone to /home/xxxxxx/.kube/config

```
3. run an initial manual deployment
```
deploy-cowsay-latest.sh
```
4. delete the cluster
```
delete-cluster.sh
```

## inspect rollout / history

various useful commands...
```
kubectl get pods -o wide

kubectl get pods --all-namespaces -o jsonpath="{..image}"

kubectl rollout status deployment cowsay-web-rolling-update

kubectl get deployment cowsay-web-rolling-update
```

## CircleCI env variables

| name                    | content                                       |
|-------------------------|-----------------------------------------------|
| DOCKER_ID               | docker.io user/login                          |
| DOCKER_PASSWORD         | docker.io user/login password                 |
| AWS_ACCESS_KEY_ID       | service access user key id                    |
| AWS_SECRET_ACCESS_KEY   | service access user key                       |
| AWS_DEFAULT_REGION      | AWS region, eu-central-1                      |
| EKS_CLUSTER_NAME        | name of the AWS EKS cluster, udacity-capstone |

# how the deployment works

- the _Dockerfile_ in _k8s/deployment\_container_ is used to build a container containing eksctl, aws-iam-authenticator and kubectl
- _k8s/deployment\_container_ also contains scripts to
  - build the container: _build-container.sh_
  - publish the container to dockerhub: _push-container.sh_
- as this image is static it is not build in the pipeline
  - a changing version of the tool could cause issues - so if something changes a manual update must be done
- the container runs a script (_k8s/deployment\_containe/deploy.sh_) 
  - expects a deployment config as input on stdin and writes it to _deployment.yml_
  - enables access for kubectl to the cluster
  - runs kubectl to update the deployment
- the related template file can be found at: _k8s/cowsay-deployment-template.yml
- there is a job named _deploy-new-image_ that runs the image by piping in the _k8s/cowsay-deployment-template.yml_
  - _sed_ is used to prepare a per build _/tmp/deployment.${DOCKER_TAG}.yml_ file
