import os
import uuid
from django.conf import settings
from django.shortcuts import render
from wand.image import Image
from wand.drawing import Drawing
from django.http import HttpRequest, HttpResponse, FileResponse

def index(request: HttpRequest):
    resp = render(request, "Page.html", context={})
    gid = request.COOKIES.get('gid')
    if not gid:
        gid_ = str(uuid.uuid4())
        resp.set_cookie("gid", gid_)
        os.mkdir(f'{ settings.BASE_DIR }/images/{ gid_ }')
    return resp


def result(request: HttpRequest):
    gid = request.COOKIES.get('gid')
    if not gid:
        gid_ = str(uuid.uuid4())
        resp.set_cookie("gid", gid_)
    bg_img = request.FILES.get('bg-img')
    mk_text = request.POST.get('mk-text')
    with Image(blob=bg_img) as img:
        with Drawing() as ctx:
            ctx.font_family = 'Times New Roman'
            ctx.font_size = (img.height // 6) * 1.75
            ctx.fill_color = '#e68fd9'
            ctx.fill_opacity = 0.4
            img.annotate(mk_text, ctx, left=40, baseline=img.height // 3)
        img.save(filename=f'{settings.BASE_DIR}/images/{ gid }/{bg_img}')
    ctx = {"file_name": bg_img.name.split('.')[0]}
    return render(request, "Item.html", context=ctx)

def download(request: HttpRequest):
    filename = request.GET["filename"]
    gid = request.COOKIES.get("gid")
    if filename:
        resp = FileResponse(open(f'{ settings.BASE_DIR }/images/{ gid }/{filename}.jpg', 'rb'))
        resp["content-type"] = "image/jpeg"
        resp["content-disposition"] = "attachment"
        return resp