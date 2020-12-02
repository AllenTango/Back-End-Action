from dominate.document import document
from dominate.tags import *


css   = "https://cdn.jsdelivr.net/npm/tailwindcss/dist/tailwind.min.css"
doc = document()
with doc:
    with doc.head:
        link(rel="stylesheet",href=css)
    with doc.body:
        attr(cls="bg-black")
    with doc:


        with div(cls="min-h-screen flex justify-center items-center flex-col"):
            img(src="https://file-hjvdnhtoxy.now.sh")
            with form(cls="flex mt-3"):
                attr(
                    action='/result',
                    method='post'
                )

                input_(name="code",cls="border-2 w-64 py-2 px-3 text-white text-4xl justify-center bg-black"),
                button("SUBMIT",cls="bg-white py-2 px-3 text-4xl justify-center")

