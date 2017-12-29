# Backend
This is the backend :)

![build-status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiekZnWGx1a2k3Z2xLQnd6Q1h5SG1Tc1Z4RE5nbUZvTXdEUERzc2k0S3EvOEpQVVNkcis1amRoZ20weU92K1prbmowOFNyaGdNdjZnZzJJRlo0c1dqRE9ZPSIsIml2UGFyYW1ldGVyU3BlYyI6Ik5aWUhLN1g2SU5qVTBoMHMiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## TODO
 * ~~enable Scheduling~~
 * ~~enable notifications~~
 * ~~use custom user-agent~~
 * ~~limit notifications (e.g. when service is down, do not send it every 15min)~~
 * enable "passive" monitoring (service notifies us about status)
 * conditional updates when writing to dynamodb?
 * contact AWS support to get out of SES sandbox
 * other notification types
 * current testing/deployment process is a mess. can we get CodeBuild to run some tests before deployment?
 * frontend
 * use SNS and a DeadLetterQueue instead of async lambda calls?
 * split lambda code into different zips to make them smaller? (is the size a cost-factor on AWS?)
 * ...

## Notes to self:

### (Developer) Setup
```bash
python3 -m venv venv
. ./venv/bin/activate
pip install awscli
aws configure
...
```

### Keys
```bash
aws kms create-key
aws kms encrypt --key-id THE-KEY-ID --plaintext "some secret stuff..."
```

### Deployment
 * `./deploy.sh`

### Notes
 * https://github.com/awslabs/serverless-application-model/blob/master/HOWTO.md
 * https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md
 * https://cloudonaut.io/integrate-sqs-and-lambda-serverless-architecture-for-asynchronous-workloads/
 * http://docs.aws.amazon.com/sns/latest/dg/sns-lambda.html
