from PIL import Image
import numpy as np
from django.shortcuts import render
from django.views.generic import View
from .forms import PictureForm
from .models import PictureFile
from .dl_model import SegmentModel, resize
# Create your views here.

model = SegmentModel()


class SegmentationPicture(View):
    def get(self, request):
        form = PictureForm()
        return render(request, 'segm_page/upload.html', context={'form': form})

    def post(self, request):
        bound_form = PictureForm(files=request.FILES)
        if bound_form.is_valid():
            image = bound_form.cleaned_data['image']
            image_name = image.name.split('.')[0]
            or_img = Image.open(image.file).convert('RGB')
            # dl model
            segm_img = model.find_segment(or_img)
            or_img = np.array(resize(or_img))
            # save to ORM
            new_obj = PictureFile(or_image=(image_name, or_img),
                                  segm_image=('segm_' + image_name, segm_img))
            new_obj.save()
            return render(request, 'segm_page/view_segment.html', context={'form': bound_form,
                                                                           'content_images': new_obj})

        return render(request, 'segm_page/upload.html', context={'form': bound_form})
