import boto3
import os
import urllib.parse

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["DYNAMODB_TABLE"])

    for record in event["Records"]:
        s3_info = record["s3"]
        object_key = s3_info["object"]["key"]
        company, soft, _ = urllib.parse.unquote(object_key).split("/", 2)
        response = table.put_item(
            Item={
                "company": company,
                "soft": soft
            }
        )
        print(response)

    return
