import sys
from django.db import models
from PIL import Image
from io import BytesIO
from time import time
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.files.uploadedfile import InMemoryUploadedFile
# Create your models here.


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class PictureFile(models.Model):
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    or_image = models.ImageField(upload_to='or_images/')
    segm_image = models.ImageField(upload_to='segm_images/')

    def save(self, *args, **kwargs):
        if not self.id:
            self.or_image = self.compress_image(self.or_image)
            self.segm_image = self.compress_image(self.segm_image)
            self.slug = gen_slug(self.or_image.name)
        super().save(*args, **kwargs)

    def compress_image(self, uploaded_image: tuple):
        image_temp = Image.fromarray(uploaded_image[1].astype('uint8'))
        output_io_stream = BytesIO()
        image_temp.save(output_io_stream, format='JPEG')
        output_io_stream.seek(0)
        uploaded_image = InMemoryUploadedFile(output_io_stream, 'ImageField',
                                             "{}.jpg".format(uploaded_image[0]),
                                             'image/jpeg', sys.getsizeof(output_io_stream), None)
        return uploaded_image

    def get_absolute_url(self):
        return reverse('segmentation_load', kwargs={'slug': self.slug})

    def __str__(self):
        return self.or_image.name