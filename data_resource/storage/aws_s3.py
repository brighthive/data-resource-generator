import logging
import boto3
import json
from botocore.exceptions import ClientError

# will upload a file from volume to a s3 bucket
def aws_s3_upload_file(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client("s3")
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# will check if s3 object exist in s3
def aws_s3_object_exists(bucket, object_name):
    try:
        s3_resource = boto3.resource("s3")
        s3_resource.Object(bucket, object_name).load()
    except ClientError as e:
        return int(e.response["Error"]["Code"]) != 404
    return True


# will get uploaded dat from s3 bucket object (utf-8 decoding)
def aws_s3_get_data(bucket, object_name):
    try:
        s3 = boto3.resource("s3")
        obj = s3.Object(bucket, object_name)
        data = obj.get()["Body"].read().decode("UTF-8")
        return data
    except ClientError as e:
        return None


# will upload json_data to a bucket with object name (utf-8 encoding)
def aws_s3_put_data(json_data, bucket, object_name):
    try:
        s3 = boto3.resource("s3")
        obj = s3.Object(bucket, object_name)
        obj.put(Body=(bytes(json.dumps(json_data).encode("UTF-8"))))
        return True
    except ClientError as e:
        return False
