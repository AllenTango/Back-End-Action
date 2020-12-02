from django_micro import route, run, configure
from dominate.document import document
import dominate.tags as dom
from wand.image import Image
from wand.drawing import Drawing
from django.http import HttpRequest, HttpResponse, FileResponse

DEBUG = True
configure(locals())

def page():
    doc = document()
    with doc as root:
        with doc.body:
            with dom.form(action='/file',method='post',enctype='multipart/form-data'):
                dom.input(type='file',name='image')
                dom.button('提交',type='submit')
    return root.render()

@route('')
def index(request:HttpRequest):
    return HttpResponse(page())

@route('file')
def filehandler(request:HttpRequest):
    user_image = request.FILES.get('image')
    # Image打开需指定类型，上传的临时文件为二进制文件
    with Image(blob=user_image) as img:
        with Drawing() as ctx:
            ctx.font_family = 'Times New Roman'
            ctx.font_size = (img.height // 6) * 1.75
            ctx.fill_color = '#e68fd9'
            ctx.fill_opacity = 0.4
            img.annotate('Water\nmelon\nMark', ctx, left=40, baseline=img.height // 3)
        img.save(filename='water-marked.jpg')
    resp = FileResponse(open('water-marked.jpg','rb'))
    resp["content-type"] = "image/jpeg"
    # resp["content-disposition"] = "attachment"
    return resp

app = run()