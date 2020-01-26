from django.conf.urls import url
from .views import SegmentationPicture

urlpatterns = [
    url('', SegmentationPicture.as_view(), name='segmentation-pic')
]