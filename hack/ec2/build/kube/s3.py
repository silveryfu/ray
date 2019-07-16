import boto3
import os
import json
from typing import List

import botocore
import botocore.errorfactory
import botocore.client


s3 = boto3.client('s3')
s3_res = boto3.resource('s3')


def create_bucket(bucket_name: str):
    s3.create_bucket(
        ACL='private',
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'us-west-1',
        },
    )


def bucket_exist(bucket: str):
    try:
        s3_res.meta.client.head_bucket(Bucket=bucket)
        return True
    except botocore.client.ClientError:
        return False


def empty_bucket(bucket_name: str):
    bucket = s3_res.Bucket(bucket_name)
    bucket.objects.all().delete()


def delete_bucket(bucket_name: str):
    bucket = s3_res.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()


def create_dir(bucket_name: str, dir_name: str):
    s3.put_object(
        Bucket=bucket_name,
        Key=(dir_name + "/")
    )


def get_object(bucket: str, prefix: str):
    # Since the key is not known ahead of time, we need to get the
    # object's summary first and then fetch the object
    bucket = s3_res.Bucket(bucket)
    objs = [i for i in bucket.objects.filter(Prefix=prefix)]

    return objs[0].get()["Body"].read()


def get_object_last_mod_time(bucket: str, prefix: str):
    bucket = s3_res.Bucket(bucket)
    objs = [i for i in bucket.objects.filter(Prefix=prefix)]

    return objs[0].last_modified


def create_local_file(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    open(path, "w").close()


def list_buckets() -> List[str]:
    # Call S3 to list current buckets
    response = s3.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket['Name'] for bucket in response['Buckets']]

    # Print out the bucket list
    # print("Bucket List: %s" % buckets)
    return buckets


def get_addr_from_bucket_key(bucket, key):
    return "s3a://" + bucket + "/" + key
