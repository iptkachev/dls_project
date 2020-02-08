from django.urls import path
from django.conf.urls import url
from .views import SegmentationCreate, SegmentationLoad

urlpatterns = [
    url('create', SegmentationCreate.as_view(), name='segmentation_create'),
    path(r'<slug:slug>', SegmentationLoad.as_view(), name='segmentation_load')
]