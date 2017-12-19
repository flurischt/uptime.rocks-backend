#!/bin/bash

# package
aws cloudformation package \
 --template-file ./backend.yml \
 --s3-bucket uptime-rocks-backend \
 --output-template-file packaged-template.yml

if [ $? -ne 0 ]; then
  echo "packaging failed. not deploying..."
  exit
fi

# and deploy
aws cloudformation deploy  \
 --template-file ./packaged-template.yml \
 --stack-name uptime-rocks \
 --capabilities CAPABILITY_IAM
