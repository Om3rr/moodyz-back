from io import BytesIO

import PIL
import cloudinary.uploader as CloudinaryUploader
from PIL import Image
from cloudinary import CloudinaryImage


class ProfilePicUploader(object):
    PROFILE_PIC_MAX_SIZE = 500

    @classmethod
    def upload(cls, image):
        pil_image = Image.open(image.stream)
        resized_pil_image = cls._resize(pil_image)
        return cls._upload(
            resized_pil_image,
        )

    @classmethod
    def _resize(cls, image):
        h, w = cls.get_new_scale(image)
        return image.resize((h, w), PIL.Image.NEAREST)

    @classmethod
    def get_new_scale(cls, image):
        h, w = image.size
        if h > w:
            scale = cls.PROFILE_PIC_MAX_SIZE / w
            return round(h * scale), cls.PROFILE_PIC_MAX_SIZE
        scale = cls.PROFILE_PIC_MAX_SIZE / h
        return cls.PROFILE_PIC_MAX_SIZE, round(w * scale)

    @classmethod
    def _upload(cls, image, **options):
        image_file = BytesIO()
        image.save(image_file, format=image.format or "PNG")
        image_data = image_file.getvalue()
        transformation = [
            {'width': 400, 'height': 400, 'gravity': "face", 'radius': "max", 'crop': "crop"},
            {'width': 120, "height": 120, 'crop': "scale"}
        ]
        options["eager"]=transformation
        result = CloudinaryUploader.upload(image_data, **options)
        return result


class ProfilePicFetcher(object):
    @classmethod
    def fetch(cls, image_id):
        return CloudinaryImage(image_id).image(transformation=[
            {'width': 400, 'height': 400, 'gravity': "face", 'radius': "max", 'crop': "crop"},
            {'width': 120, "height": 120, 'crop': "scale"}
        ]).replace("<img src=\"", "").replace("\"/>", '')
