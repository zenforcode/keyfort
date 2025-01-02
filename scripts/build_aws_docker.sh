#!/bin/bash
AWS_REGION="us-east-1"
REPO_NAME="zenforcode"    
IMAGE_NAME="keyfort"     
TAG="latest"
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $1.dkr.ecr.$AWS_REGION.amazonaws.com
docker build -t $IMAGE_NAME .
docker tag $IMAGE_NAME:latest <AWS_ACCOUNT_ID>.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$TAG
docker push $1.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$TAG
echo "Docker image pushed to ECR: $1.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME:$TAG"
