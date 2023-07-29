from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import math


def custom_img(img_field, max_width=0, aspect_ratio=0):
    if img_field:
        name = img_field.name.split('.')[0]
        height = img_field.height
        width = img_field.width

        img = Image.open(img_field)

        if img.format != 'webp':
            img_io = BytesIO()
            if max_width and width > max_width:
                height = math.floor(height * (max_width / width))
                width = math.floor(max_width)

                img = img.resize((width, height), Image.ANTIALIAS)

            if width/height > aspect_ratio:
                width = math.floor(height * aspect_ratio)
                x = math.floor((img.width - width) / 2)

                img = img.crop((x, 0, width + x, height))

            elif width/height < aspect_ratio:
                height = math.floor(width / aspect_ratio)
                x = 0

                img = img.crop((x, 0, width + x, height))

            img.save(img_io, format='webp')

            new_img = InMemoryUploadedFile(
                file=img_io,
                field_name= img_field.field.name,
                name=f'{name}.webp',
                content_type='image/webp',
                size=img_io.getbuffer().nbytes,
                charset=None
            )

            return new_img

        else:
            img.close()
            return img_field
    else: return None