from django_micro import route, run, configure
from dominate.document import document
import dominate.tags as dom
from wand.image import Image
from django.http import HttpRequest, HttpResponse, FileResponse

DEBUG = True
configure(locals())

def page():
    doc = document()
    with doc as root:
        with doc.body:
            with dom.form(action='/file',method='post',enctype='multipart/form-data'):
                dom.label('上传原图')
                dom.input(type='file',name='bg_image')
                dom.label('上传水印图')
                dom.input(type='file',name='mk_image')
                dom.button('提交',type='submit')
    return root.render() 

@route('')
def index(request:HttpRequest):
    return HttpResponse(page())

@route('file')
def filehandler(request:HttpRequest):
    bg_image = request.FILES.get('bg_image')
    mk_image = request.FILES.get('mk_image')
    # Image打开需指定类型，上传的临时文件为二进制文件
    with Image(blob=bg_image) as bg_img:
        with Image(blob=mk_image) as mk_img:
            # bg_img.composite(mk_img)
            bg_img.watermark(mk_img, transparency=0.5)
        bg_img.save(filename=f'{bg_image.name}')

    resp = FileResponse(open(f'{bg_image.name}','rb'))
    resp["content-type"] = "image/jpeg"
    # resp["content-disposition"] = "attachment"
    return resp

app = run()