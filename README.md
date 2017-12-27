# Backend
This is the backend :)

![build-status](https://codebuild.eu-central-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiekZnWGx1a2k3Z2xLQnd6Q1h5SG1Tc1Z4RE5nbUZvTXdEUERzc2k0S3EvOEpQVVNkcis1amRoZ20weU92K1prbmowOFNyaGdNdjZnZzJJRlo0c1dqRE9ZPSIsIml2UGFyYW1ldGVyU3BlYyI6Ik5aWUhLN1g2SU5qVTBoMHMiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)

## TODO
 * enable Scheduling
 * use SNS and a DeadLetterQueue instead of async lambda calls?
 * ...

## Notes to self:

### Setup
```bash
python3 -m pip install awscli
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