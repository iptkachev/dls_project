from PIL import Image
import numpy as np
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .forms import PictureForm
from .models import PictureFile
from .dl_model import SegmentModel, resize
# Create your views here.

model = SegmentModel()


class SegmentationCreate(View):
    def get(self, request):
        form = PictureForm()
        return render(request, 'segm_page/upload.html', context={'form': form})

    def post(self, request):
        bound_form = PictureForm(files=request.FILES)
        if bound_form.is_valid():
            image = bound_form.cleaned_data['image']
            image_name = image.name.split('.')[0]
            with Image.open(image.file) as image_file:
                or_img = image_file.convert('RGB')
            # dl model
            segm_img = model.find_segment(or_img)
            or_img = np.array(resize(or_img))
            # save to ORM
            new_obj = PictureFile(or_image=(image_name, or_img),
                                  segm_image=('segm_' + image_name, segm_img))
            new_obj.save()
            return redirect(new_obj)
        return render(request, 'segm_page/upload.html', context={'form': bound_form})


class SegmentationLoad(View):
    def get(self, request, slug):
        form = PictureForm()
        obj = get_object_or_404(PictureFile, slug=slug)
        return render(request, 'segm_page/view_segment.html', context={'form': form,
                                                                       'content_images': obj})
