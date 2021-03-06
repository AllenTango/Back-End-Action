import base64
import dominate.tags as dom
from wand.image import Image
from wand.drawing import Drawing
from dominate.document import document
from django_micro import route, run, configure
from django.http import HttpRequest, HttpResponse, FileResponse


CENTER_FRAME = "flex flex-col items-center justify-center bg-blue-200 min-h-screen"
IMG_CARD = "flex flex-col bg-white shadow-xl p-3 rounded-lg w-120 h-120 p-2"
LABEL_CARD = "flex flex-col bg-green-400 w-120 h-24 p-2 mb-2 rounded-lg shadow-xl"
LABEL_INPUT = "h-10 rounded border-none p-4 text-center text-xl text-gray-600 placeholder-gray-400 outline-none focus:shadow-outline"
IMG_FORM = "flex flex-col items-center justify-center border-dashed border-4 border-gray-200 h-full"
FORM_ATTR = {
    "ic-post-to": "/file",
    "ic-target": "#here",
    "ic-replace-target": "true",
    "enctype": "multipart/form-data"}
UPLOAD_ICON = "fas fa-file-upload text-gray-300 font-medium text-6xl"
BUTTON = "flex flex-row items-center justify-center bg-green-400 px-3 py-2 mt-4 text-white rounded shadow"
RESULT_CONTAINER = "flex flex-col"
RESULT_ITEM = "flex flex-col items-center justify-between bg-white p-4 border-t border-gray-200 w-96"

configure({'DEBUG': True})


def link_(lk):
    return dom.link(rel="stylesheet", type="text/css", href=lk)


def script_(s):
    return dom.script(src=s)


def page():
    doc = document()
    with doc.head:
        link_("https://unpkg.com/tailwindcss@^1.0/dist/tailwind.min.css")
        link_("https://extra-uru1z3cxu.now.sh/css/extra.css")
        link_("https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.2/css/all.css")
        script_("https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js")
        script_("http://intercoolerjs.org/release/intercooler-1.2.2.js")

    with doc.body:
        with dom.div(cls=CENTER_FRAME) as CenterFrame:
            with dom.form(FORM_ATTR):
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

            with dom.div(cls=RESULT_CONTAINER, id="there") as ResultContainer:
                dom.span(id="here")
    
    return doc.render()

def Item(file_name):
    with open(f'{file_name}.jpg', 'rb') as img_file:
        b64_str = base64.b64encode(img_file.read())
    with dom.div(cls=RESULT_ITEM) as ResultItem:
        dom.p(f"{ file_name }.jpg", {"ic-action": "slideToggle", "ic-target": f"#{file_name}"}, cls="w-full text-xl text-gray-400")
        dom.img(src=f"data:image/jpeg;base64,{b64_str.decode('utf-8')}", id=f"{file_name}", cls="w-full", style="display:none")

    return ResultItem.render() + dom.span(id="here").render()


@route('')
def index(request: HttpRequest):
    return HttpResponse(page())


@route('file')
def result(request: HttpRequest):
    bg_img = request.FILES.get('bg-img')
    mk_text = request.POST.get('mk-text')
    with Image(blob=bg_img) as img:
        with Drawing() as ctx:
            ctx.font_family = 'Times New Roman'
            ctx.font_size = img.height // 6
            ctx.fill_color = '#e68fd9'
            ctx.fill_opacity = 0.8
            img.annotate(mk_text, ctx, left=40, baseline=img.height // 3)
        img.save(filename=f'{bg_img.name.split(".")[0]}.jpg')
    return HttpResponse(Item(f'{bg_img.name.split(".")[0]}'))

app = run()
