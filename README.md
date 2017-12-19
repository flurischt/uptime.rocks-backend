# Backend
This is the backend :)

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