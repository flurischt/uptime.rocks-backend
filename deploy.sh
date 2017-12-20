#!/bin/bash

# get requirements and put everything into code.zip
echo packaging code.zip
python3.6 -m pip install -q --upgrade -r code/requirements.txt -t code/
cd code/ && zip ../code.zip -qr ./ && cd ..

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
