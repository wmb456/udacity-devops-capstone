FROM python:3.9.2-alpine3.12

WORKDIR /app

RUN apk add --update --no-cache curl groff

RUN curl --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" -o eksctl.tar.gz && tar -xzf eksctl.tar.gz && \
    rm eksctl.tar.gz && \
    chmod +x eksctl && \
    mv eksctl /usr/local/bin && \
    eksctl version

RUN curl --location https://storage.googleapis.com/kubernetes-release/release/v1.20.0/bin/linux/amd64/kubectl -o kubectl && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin && \
    kubectl version --client=true

RUN curl --location https://amazon-eks.s3.us-west-2.amazonaws.com/1.19.6/2021-01-05/bin/linux/amd64/aws-iam-authenticator -o aws-iam-authenticator && \
    chmod +x aws-iam-authenticator && \
    mv aws-iam-authenticator /usr/local/bin && \
    aws-iam-authenticator version

RUN pip install awscli==1.19.5 && \
    aws help > /dev/null

COPY deploy.sh .

CMD ["/bin/sh", "deploy.sh"]
