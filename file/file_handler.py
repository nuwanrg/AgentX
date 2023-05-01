import boto3

def upload_file_to_s3(file_object, bucket_name, s3_object_name):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        response = s3.upload_fileobj(file_object, bucket_name, s3_object_name)
        print('response ', response)
        print(f"File uploaded to {bucket_name}/{s3_object_name}")
        return response
    except Exception as e:
        print(f"Error uploading file: {e}")
        return None


def generate_s3_url(bucket_name, object_name):
    s3 = boto3.client('s3')
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=3600  # URL will be valid for 1 hour; adjust as needed
    )
    return url

# Example usage
# media_id = 'your-whatsapp-media-id'
# access_token = 'your-access-token'
# bucket_name = 'your-s3-bucket-name'
# s3_object_name = f"{media_id}.jpg"  # Change the file extension if needed

# file_object = download_file_from_whatsapp(media_id, access_token)
# if file_object:
#     upload_file_to_s3(file_object, bucket_name, s3_object_name)
