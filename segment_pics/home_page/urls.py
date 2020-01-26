from django.conf.urls import url
from .views import start

urlpatterns = [
    url('', start, name='start_page')
]