Flask on Kubernetes
=======
# Sample REST API running on Kubernetes
This is a REST API that modifies users in DynamoDB. The API runs on Kubernetes.
This sample was designed to run on Elastic Container Service (EKS), although it coulud work in other clusters.

To deploy the API in other clusters you will have to modify the deployment.yaml to provide the AWS Credentials using secrets or any other method so the AWS SDK can get the credentials to manage DynamoDB.

# How it works:
Once deployed the API will listen on port 80, using as entry point a Load Balancer service. The load balancer forwards the requests to a replica with 2 pods.

# How to deploy on Amazon EKS:
1) Create a DynamoDB:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/SQLtoNoSQL.CreateTable.html

Create a table with primary key ```id``` type String.

2) Modify people.py and set your region and DynamoDB name.

```python
REGION = 'us-west-2'
TABLE_NAME = 'peopledb'
```

3) Create image and push it to your repository.

```bash
docker build . -t api:latest
```

Push your image to your Docker Repository (I pushed the image to my own public repository).

4) Edit deployment.yaml
```yaml
        image: YOUR REPO
```

5) Make sure that you provide AWS credentials to the SDK image.
If you run this sample in AWS, add the following policy to the IAM role of your worker nodes:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "ListAndDescribe",
            "Effect": "Allow",
            "Action": [
                "dynamodb:List*",
                "dynamodb:DescribeReservedCapacity*",
                "dynamodb:DescribeLimits",
                "dynamodb:DescribeTimeToLive"
            ],
            "Resource": "*"
        },
        {
            "Sid": "SpecificTable",
            "Effect": "Allow",
            "Action": [
                "dynamodb:BatchGet*",
                "dynamodb:DescribeStream",
                "dynamodb:DescribeTable",
                "dynamodb:Get*",
                "dynamodb:Query",
                "dynamodb:Scan",
                "dynamodb:BatchWrite*",
                "dynamodb:CreateTable",
                "dynamodb:Delete*",
                "dynamodb:Update*",
                "dynamodb:PutItem"
            ],
            "Resource": "arn:aws:dynamodb:*:*:table/TABLE NAME HERE"
        }
    ]
}
```
Make sre you change the table name in the policy.

IMPORTANT:
If you want to work with Pod level credentails instead of node level credentials check out this project:
https://github.com/helm/charts/tree/master/stable/kube2iam

6) Deploy the deployment and service:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```

# STUFF TO FIX
- Right now the API accepts only integers in the fare field (I have to cast the values to Decimal.decimal so that Dynamo catches it without exception.

# TODOS
- Create Helm chart.
- Create table on deployment.
- Integrate with Kube2IAM or any other resources as right now credentials are retrieved from Instance role at host level.

# Contains:
- Swagger definition
- Python running Connexion Framework
- Service and deployment definition.
- Dockerfile
