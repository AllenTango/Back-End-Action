from django_micro import configure, route, run
from django.http import HttpResponse

setting = {
    "DEBUG": True,
    "LANGUAGE_CODE": 'en-us'
}
configure(setting)

source = "APR 6, PNC ARENA, RALEIGH,NC/APR 7, STATE FARM ARENA, ATLANTA,GA/APR 9, BRIDGESTONE ARENA, NASHVILLE,TN/APR 11, AMALIE ARENA, TAMPA,FL"

data = ''
for s in source.split('/'):
    data += f'''
        <tr style="border-top:1pt solid #555555">
            <td><h3> {s.split(',')[0]} </h3></td>
            <td><h3> {s.split(',')[1]} </h3></td>
            <td><h3> {s.split(',')[2]} {s.split(',')[3]} </h3></td>
        </tr>'''
# print(data)
@route('', name='home')
def homepage(request):
    html = f'''
    <div style="background-color:#0A0A0E;height:100%">
        <image src="https://file-rctyjgetlr.now.sh" style="height:70%;margin:auto;display:block">
        <table style="width:60%;color:white;border-collapse:collapse" align="center">
            { data }
        </table>
    </div>'''
    return HttpResponse(html)


application = run()