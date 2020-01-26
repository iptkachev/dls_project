from rest_framework import serializers
from .models import PictureFile


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PictureFile
        fields = '__all__'
