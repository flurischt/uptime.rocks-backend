#!/bin/bash

#
# this script is for deploying from a developer-machine. 
# usually the deployment is done using CodeBuild and buildspec.yml
#

# we'll use pylint and awscli in the virtualenv
. ./venv/bin/activate

function package {
        # get requirements and put everything into code.zip
        echo packaging code.zip
        rm -rf code/requirements/*
        touch code/requirements/.gitkeep
        pip install -q --upgrade -r code/requirements.txt -t code/requirements/

        PYTHONPATH=code/requirements/ pylint -E code/uptime
        if [ $? -ne 0 ]; then
          echo "pylint reported errors! Not deploying..."
          exit
        fi

        # add our code and the requirements/ directory to the zip
        cd code/ 
        zip ../code.zip -qr ./uptime ./local_secrets.py
        cd requirements/
        zip ../../code.zip --grow -qr ./*
        cd ../../
}

git status code/ | grep "nothing to commit, working directory clean" > /dev/null
if [ $? -eq 0 ]; then
    if [ -f code.zip ]; then
        echo "no code-changes. redeploying existing code.zip"
    else
        package
    fi
else
    package
fi

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

# exit virtualenv
deactivate
