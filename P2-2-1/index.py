from dominate.document import document
import dominate.tags as dom
from wand.image import Image
from wand.drawing import Drawing
from django_micro import route, run, configure
from django.http import HttpRequest, HttpResponse, FileResponse


CENTER_FRAME = "flex flex-col items-center justify-center bg-blue-200 h-screen"
IMG_CARD = "flex flex-col bg-white shadow-xl p-3 rounded-lg w-120 h-120 p-2"
LABEL_CARD = "flex flex-col bg-green-400 w-120 h-24 p-2 mb-2 rounded-lg shadow-xl"
LABEL_INPUT = "h-10 rounded border-none p-4 text-center text-xl text-gray-600 placeholder-gray-400 outline-none focus:shadow-outline"
IMG_FORM = "flex flex-col items-center justify-center border-dashed border-4 border-gray-200 h-full"
UPLOAD_ICON = "fas fa-file-upload text-gray-300 font-medium text-6xl"
BUTTON = "flex flex-row items-center justify-center bg-green-400 px-3 py-2 mt-4 text-white rounded shadow"
RESULT_CONTAINER = "flex flex-col"
RESULT_ITEM = "flex flex-row items-center justify-between bg-white p-4 border-t border-gray-200 w-96"

configure({'DEBUG': True})


def link_(lk):
    return dom.link(rel="stylesheet", type="text/css", href=lk)


def page():
    doc = document()
    with doc.head:
        link_("https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css")
        link_("https://extra-uru1z3cxu.now.sh/css/extra.css")
        link_("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.css")
        dom.script(
            src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js')

    with doc.body:
        with dom.div(cls=CENTER_FRAME) as CenterFrame:
            with dom.form(action='/file', method='post', enctype='multipart/form-data'):
                with dom.div(cls=LABEL_CARD):
                    dom.label('Write down your mark here',
                              cls="text-white text-xl")
                    dom.input(
                        cls=LABEL_INPUT, type='text', placeholder='your watermark text here', name='mk-text')
                with dom.div(cls=IMG_CARD):
                    with dom.div(cls=IMG_FORM):
                        dom.i(cls=UPLOAD_ICON,
                              onclick='''$('#fileupload').click()''')
                        dom.p("Find File", id="file", cls="text-gray-500 mt-4")
                        dom.input(cls="hidden", type="file", name='bg-img', id="fileupload",
                                  onchange='''$('#file').text(this.value.split("\\\\").pop(-1))''')
                        dom.button('Upload', cls=BUTTON, type='submit')

            with dom.div(cls=RESULT_CONTAINER) as ResultContainer:
                for _ in range(4):
                    with dom.div(cls=RESULT_ITEM) as ResultItem:
                        dom.p("filename.jpg", cls="text-xl text-gray-400")
                        dom.i(cls="fas fa-download text-xl text-gray-400")

    return doc.render()


@route('')
def index(request: HttpRequest):
    return HttpResponse(page())


@route('file')
def filehandler(request: HttpRequest):
    bg_img = request.FILES.get('bg-img')
    mk_text = request.POST.get('mk-text')
    with Image(blob=bg_img) as img:
        with Drawing() as ctx:
            ctx.font_family = 'Times New Roman'
            ctx.font_size = (img.height // 6) * 1.75
            ctx.fill_color = '#e68fd9'
            ctx.fill_opacity = 0.4
            img.annotate(mk_text, ctx, left=40, baseline=img.height // 3)
        img.save(filename='water-marked.jpg')
    resp = FileResponse(open('water-marked.jpg', 'rb'))
    resp["content-type"] = "image/jpeg"
    # resp["content-disposition"] = "attachment"
    return resp


app = run()
