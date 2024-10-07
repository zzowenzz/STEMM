import boto3
import random
from PIL import Image
import streamlit as st
import requests

# Initialize a session using boto3 and provide your AWS credentials securely using Streamlit secrets
s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name=st.secrets["AWS_REGION"]
)

# Define the bucket name from Streamlit secrets
BUCKET_NAME = st.secrets["S3_BUCKET_NAME"]

# Koala classes (subdirectories in your S3 bucket under the main images directory)
koala_classes = ["DES_alana", "DES_alex", "DES_ally", "DES_anke"]

# Get pre-signed URLs for reference images for a koala class
def get_reference_images(koala_class):
    # List objects in the S3 bucket under the koala class folder
    prefix = f"images/{koala_class}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    
    # Filter for reference images
    reference_images = [
        obj['Key'] for obj in response.get('Contents', [])
        if 'reference' in obj['Key']
    ]
    random.shuffle(reference_images)  # Shuffle the order of reference images
    
    # Generate pre-signed URLs for the images
    reference_image_urls = [
        s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': image_key},
            ExpiresIn=3600  # URL expiration time in seconds
        )
        for image_key in reference_images
    ]
    return reference_image_urls

# Get a pre-signed URL for a random unseen image for a quiz (we will pick a random unseen image for each user)
def get_quiz_image(koala_class):
    # List objects in the S3 bucket under the koala class folder
    prefix = f"images/{koala_class}/"
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    
    # Filter for unseen images
    unseen_images = [
        obj['Key'] for obj in response.get('Contents', [])
        if 'unseen' in obj['Key']
    ]
    if unseen_images:
        random_image_key = random.choice(unseen_images)
        quiz_image_url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': random_image_key},
            ExpiresIn=3600  # URL expiration time in seconds
        )
        return quiz_image_url
    return None

# Get all koala classes
def get_koala_classes():
    return koala_classes

# Resize images using PIL (if needed, for example, resizing fetched images from S3)
def resize_image(image_url, size=(50, 50)):
    # Download the image directly from the URL
    img = Image.open(requests.get(image_url, stream=True).raw)
    return img.resize(size)
