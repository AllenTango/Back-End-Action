from django_micro import configure, route, run
from django.http import HttpResponse
from django.http import HttpRequest
import csv

setting = {
    'DEBUG': True,
    'ALLOWED_HOSTS': ["127.0.0.1"],
    'LANGUAGE_CODE': 'en-us'

}
configure(setting)

buffer = open("./source.csv", "r")
r = list(csv.reader(buffer))
data = ''

for row in r:
    data += f'''
    <tr style="border-top:1pt solid #555555">
        <td><h3> {row[0]} </h3></td>
        <td><h3> {row[1]} </h3></td>
        <td><h3> {row[2]} </h3></td>
    </tr>'''

male_ad = '<image src="https://file-fsouxucwbs.now.sh" style="height:10%;margin:auto;display:block">'
female_ad = '<image src="https://file-crccldcpvg.now.sh" style="height:10%;margin:auto;display:block">'


ref_dict = {
    "worstbuy":0.3,
    "foolmart":0.4,
    "badcoupons":0.5
}

def get_coupons(coupon):
    percent = "{0:.0f}%".format(ref_dict[coupon]*100)
    return f'''<div style="background:red;width:260px;margin:auto;font-size:30px;color:white">Click get { percent } off</div>'''


@route('', name='home')
def homepage(request:HttpRequest):
    coupon = ''
    ref = request.GET.get('ref')
    if ref:
        if ref_dict.get(ref):
            coupon = get_coupons(ref)
        else:
            return HttpResponse(ref)

    html = f'''
    <div style="background-color:#0A0A0E;height:150%">
        <image src="https://file-rctyjgetlr.now.sh" style="height:70%;margin:auto;display:block">
        { coupon }
        <table style="width:70%;color:white;border-collapse:collapse" align="center">
            {data}
        </table>
    </div>
    '''
    return HttpResponse(html)


application = run()