import boto3
import uuid
from botocore.exceptions import ClientError
from decimal import *

# DynamoDB client defined as Global, to allow connection pool reuse.
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('peopledb')

def update(uuid, person):
    try:
        table.update_item(
                UpdateExpression=("set survived=:survived, passengerClass=:passengerClass, #name=:name, sex=:sex, age=:age, "
                              "siblingsOrSpousesAboard=:siblingsOrSpousesAboard, "
                              "parentsOrChildrenAboard=:parentsOrChildrenAboard, "
                              "fare =:fare"),
            ExpressionAttributeValues={
                ":survived": person['survived'],
                ":passengerClass": person['passengerClass'],
                ":name": person['name'],
                ":sex": person['sex'],
                ":age": person['age'],
                ":siblingsOrSpousesAboard": person['siblingsOrSpousesAboard'],
                ":parentsOrChildrenAboard": person['parentsOrChildrenAboard'],
                ":fare": person['fare']
            },
            ExpressionAttributeNames={
                "#name": "name"
            },
            Key={
                "id": uuid
            }
        )
    except ClientError as error:
        print(error)
        return 'Opps something went wrong', 500
def add(person):
    try:
        table.put_item(
        Item={
            "id": str(uuid.uuid1()),
            "survived": person['survived'],
            "passengerClass": person['passengerClass'],
            "name": person['name'],
            "sex": person['sex'],
            "age": person['age'],
            "siblingsOrSpousesAboard": person['siblingsOrSpousesAboard'],
            "parentsOrChildrenAboard": person['parentsOrChildrenAboard'],
            "fare": person['fare']
        }
        )
    except ClientError as error:
        return 'Opps something went wrong', 500

# Handler to list all users
# TODO use paginators to list the whole table. Currently limited to 1MB as per DynamoDB docs.
def list():
    try:
        response = table.scan()
        return response['Items']
    except ClientError as error:
        return 'Opps something went wrong', 500

# Handler to read a person
def get(uuid):
    try:
        response = table.get_item(
        Key={
            "id": uuid
        }
        )
        if 'Item' in response:
            return response['Item']
        else:
            return 'Not Found', 404
    except ClientError as error:
        return 'Opps something went wrong', 500


def delete(uuid):
    #  DynamoDB condition expression is used to make query idempotent
    try:
        table.delete_item(
        Key={
            "id": uuid
        },
        ConditionExpression="attribute_exists(id)"

        )
    #  ConditionalCheckFailedException means item does not exist. Raise other errors.
    except ClientError as error:
        if error.response['Error']['Code'] == "ConditionalCheckFailedException":
            return 'Not found', 404
        else:
            raise
    else:
        return 'OK', 200