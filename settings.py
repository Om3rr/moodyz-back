from dotenv import load_dotenv
import logging
import os
import cloudinary as Cloud
load_dotenv()
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


Cloud.config(**{
    'cloud_name':os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.environ.get('CLOUDINARY_API_KEY'),
    'api_secret': os.environ.get('CLOUDINARY_API_SECRET')
})