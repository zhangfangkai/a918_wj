from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.template.context import RequestContext
from models import *
import uuid

def bks(req):
    wenjuan_id = 1
    wenjuan = Wenjuan.objects.filter(id=wenjuan_id)
    wenti = Wenti.objects.filter(wenjuan_id=wenjuan_id).all()
    if req.method == "GET":
        data = {}
        name = wenjuan.all()[0].wenjuan_name
        data['wj_name'] = name
        wj_data = []
        for i in wenti:
            wenti={}
            wenti_name = i.wenti_name
            wenti_type = i.wenti_type
            wenti_id = i.id
            wenti_xuhao = i.wenti_xuhao
            wenti['wenti_name'] = wenti_name
            wenti['wenti_type'] = wenti_type
            wenti['wenti_xuhao'] = wenti_xuhao
            wenti['wenti_id'] = wenti_id
            xx = []
            if wenti_type == 1 or wenti_type == 3:

                xuanxiang = Xuanxiang.objects.filter(wenti_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.xuanxiang_name
                    xuanxiang_xuhao = j.xuanxiang_xuhao
                    xxx['xuanxiang_name']=xuanxiang_name
                    xxx['xuanxiang_xuhao']=xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            wj_data.append(wenti)
        data['wj_data'] = wj_data
        print data
        return render_to_response('dxs.html', data, RequestContext(req))
    else:
        tip = uuid.uuid4()
        objs = []
        for i in range(1, wenti.count()+1):
            wenti_n = wenti.filter(wenti_xuhao=i).all()
            if wenti_n.first().wenti_type == 3:
                data = req.POST.getlist(str(i))
                print data
                if len(data) == 0:
                    return render_to_response('failed.html', RequestContext(req))
                else:
                    for d in data:
                        obj = {}
                        obj['wenti_id'] = wenti_n.first().id
                        obj['huida_data'] = d
                        objs.append(obj)
            else:
                data = req.POST.get(str(i))
                if data is None:
                    return render_to_response('failed.html', RequestContext(req))
                else:
                    obj = {}
                    obj['wenti_id'] = wenti_n.first().id
                    obj['huida_data'] = data
                    objs.append(obj)
        for i in objs:
            Huida.objects.create(wenjuan_id=wenjuan_id, wenti_id=i.get('wenti_id'), huida_data=i.get('huida_data'), huida_tip=tip)
        return render_to_response('success.html', RequestContext(req))

