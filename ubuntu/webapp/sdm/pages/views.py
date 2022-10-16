from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from os import listdir
from os.path import isfile, join
from datetime import datetime
from .models import *
import time
from django.http import HttpResponse


ip_exp_sec = 60

def get_img_names():
    files_path='/home/ubuntu/webapp/sdm/pages/static/pages/imgs/'
    onlyfiles = [f for f in listdir(files_path) if isfile(join(files_path, f))]
    return onlyfiles

def format_data():
    data = []
    
    all_imgs = get_img_names()
    for val in all_imgs:
        fd={}
        sp = val.split('---')
        ts = int(sp[0])
        fd['rep_id'] = ts
        lt = datetime.utcfromtimestamp(ts+14400).strftime('%d-%m-%Y %H:%M:%S')
        spd = lt.split(' ')
        fd['date'] = spd[0]
        fd['time'] = spd[1]
        fd['loc'] = sp[1]
        fd['gate'] = sp[2]
        fd['cam_id'] = sp[3]
        fd['img_url'] = f'/static/pages/imgs/{val}'
        data.append(fd)
    return data

# @login_required
class HomePageView(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        data = format_data()
        return {"data": reversed(data)}

def report(request):
    data = {}
    data['rep_id'] = request.GET.get('rep_id')
    data['date'] = request.GET.get('date')
    data['time'] = request.GET.get('time')
    data['loc'] = request.GET.get('loc')
    data['gate'] = request.GET.get('gate')
    data['cam_id'] = request.GET.get('cam_id')
    data['img_url'] = request.GET.get('img_url')
    return render(request, 'pages/report.html', {'data': data})

def get_ip(request):
    d = Ip.objects.all()[0]
    current_ts = int(time.time())
    last_ts = int(d.ts)
    ts_diff = current_ts - last_ts
    ip_exp = ts_diff > ip_exp_sec
    args = {'ip': d.ip, 'ts': d.ts, 'ip_exp': ip_exp, 'raw': d.raw}
    return JsonResponse(args)

def ip(request):
    d = Ip.objects.all()[0]
    args = {'ip': d.ip, 'ts': d.ts}
    return render(request, 'pages/ip.html', args)

def save_ip(request):
    ip = request.GET["ip"]
    raw = request.GET["raw"]
    Ip.objects.filter(id=1).update(
        ip=ip,
        raw=raw,
        ts = f'{int(time.time())}'
    )
    print(f"{ip}")
    return HttpResponse(f"{ip}")
