from django.db import models
from PIL import Image
from io import BytesIO
import sys
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.


class PictureFile(models.Model):
    or_image = models.ImageField(upload_to='or_images/')
    segm_image = models.ImageField(upload_to='segm_images/')

    def save(self, *args, **kwargs):
        if not self.id:
            self.or_image = self.compress_image(self.or_image)
            self.segm_image = self.compress_image(self.segm_image)
        super().save(*args, **kwargs)

    def compress_image(self, uploaded_image: tuple):
        image_temp = Image.fromarray(uploaded_image[1].astype('uint8'))
        output_io_stream = BytesIO()
        # image_temproary_resized = image_temp.resize((1020, 573))
        image_temp.save(output_io_stream, format='JPEG')
        output_io_stream.seek(0)
        uploaded_image = InMemoryUploadedFile(output_io_stream, 'ImageField',
                                             "{}.jpg".format(uploaded_image[0]),
                                             'image/jpeg', sys.getsizeof(output_io_stream), None)
        return uploaded_image

    def __str__(self):
        return self.or_image.name