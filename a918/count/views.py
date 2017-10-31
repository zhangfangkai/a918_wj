from django.shortcuts import render,render_to_response,HttpResponseRedirect
from django.template.context import RequestContext
from models import *
import operator


def main(req):
    return render_to_response('count/count.html', {}, RequestContext(req))


def tx(req):
    data = {}
    data['wjli']=wenjuan.objects.all()
    return render_to_response('count/tx.html', data, RequestContext(req))


def cx(req):
    data = {}
    wjli = wenjuan.objects.all()
    wjli2 = []
    for i in wjli:
        temp={}
        temp['id'] = i.id
        temp['wenjuan_name'] = i.wenjuan_name
        temp['num'] = Jilu.objects.filter(Jilu_tp=i.id).count()
        temp['wenjuan_status'] = i.wenjuan_status
        wjli2.append(temp)
    data['wjli'] = wjli2
    return render_to_response('count/cx.html', data, RequestContext(req))


def zy(req):
    tp = req.GET.get("tp")
    sfe = Shengfen.objects.all()

    data = {}
    slist = []
    sf = []
    for i in sfe:
        sfi = {}
        sfi['id'] = i.id
        num = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_shengfen=i.shengfen_name).count()
        sfi['num'] = num
        sfi['name'] = i.shengfen_name
        temp = {}
        if num != 0:
            temp["name"] = i.shengfen_name
            temp["num"] = num
            temp['index'] = len(slist) + 1
            slist.append(temp)
        sf.append(sfi)
    slist = sorted(slist, key=operator.itemgetter('num'), reverse=True)
    co = 1
    for i in slist:
        i['index'] = co
        co = co+1
    data["length"] = len(slist)
    data["sf"] = sf
    data["li"] = slist
    data["tp"] = tp
    data['wjname'] = wenjuan.objects.filter(id = tp)[0].wenjuan_name
    return render_to_response('count/zysf.html', data, RequestContext(req))


def xs(req):
    tp = req.GET.get("tp")
    sfe = Shengfen.objects.all()

    data = {}
    slist = []
    sf = []
    for i in sfe:
        sfi = {}
        sfi['id'] = i.id
        num = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_shengfen=i.shengfen_name).count()
        sfi['num'] = num
        sfi['name'] = i.shengfen_name
        temp = {}
        sf.append(sfi)
        if num != 0:
            temp["name"] = i.shengfen_name
            temp["num"] = num
            temp['index'] = len(slist)+1
            slist.append(temp)
    slist = sorted(slist, key=operator.itemgetter('num'), reverse=True)
    co = 1
    for i in slist:
        i['index'] = co
        co = co + 1
    data["length"] = len(slist)
    data["sf"] = sf
    data["li"] = slist
    data["tp"] = tp
    data['wjname'] = wenjuan.objects.filter(id = tp)[0].wenjuan_name
    return render_to_response('count/xssf.html', data, RequestContext(req))


def zdx(req):
    tp = req.GET.get("tp")
    sfid = req.GET.get("sfid")
    type = req.GET.get("type")

    sfname = Shengfen.objects.filter(id=sfid).all()[0].shengfen_name
    sfnum = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_shengfen=sfname).count()
    dxall = Daxue.objects.filter(shengfen_id=sfid).all()
    dxli = []
    dxli2 = []
    for i in dxall:
        dxe = {}
        num = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=i.daxue_name).count()
        dxe['name'] = i.daxue_name
        dxe['num'] = num
        dxe['id'] = i.id
        dxli.append(dxe)
        temp = {}
        if num != 0:
            temp["name"] = i.daxue_name
            temp["num"] = num
            temp['index'] = len(dxli2) + 1
            dxli2.append(temp)
    dxli2 = sorted(dxli2, key=operator.itemgetter('num'), reverse=True)
    co = 1
    for i in dxli2:
        i['index'] = co
        co = co + 1
    data = {}
    data['type'] = type
    data['tp'] = tp
    data['length'] = len(dxli2)
    data['daxue'] = dxli
    data['daxueli'] = dxli2
    data['sfnum'] = sfnum
    data['sfname'] = sfname
    data['wjname'] = wenjuan.objects.filter(id = tp)[0].wenjuan_name
    return render_to_response('count/dx.html', data, RequestContext(req))


def ml(req):
    tp = req.GET.get("tp")
    dxid = req.GET.get("dxid")
    type = req.GET.get("type")
    dxname = Daxue.objects.filter(id=dxid).all()[0].daxue_name
    mllist = []
    mllist2 = []

    if type == '1':
        ml = Zylx.objects.all()
        for i in ml:
            mle = {}
            mle['id'] = i.id
            mle['name'] = i.Zylx_name
            mle['num'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).filter(Jilu_ml=i.Zylx_name).count()
            temp = {}
            if mle['num'] != 0:
                temp["name"] = i.Zylx_name
                temp["num"] = mle['num']
                temp['index'] = len(mllist2) + 1
                mllist2.append(temp)
            mllist.append(mle)
    if type == '2':
        ml = Xsml.objects.all()
        for i in ml:
            mle = {}
            mle['id'] = i.id
            mle['name'] = i.Xsml_name
            mle['num'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).filter(Jilu_ml=i.Xsml_name).count()
            temp = {}
            if mle['num'] != 0:
                temp["name"] = i.Xsml_name
                temp["num"] = mle['num']
                temp['index'] = len(mllist2) + 1
                mllist2.append(temp)
            mllist.append(mle)
    mllist2 = sorted(mllist2, key=operator.itemgetter('num'), reverse=True)
    co = 1
    for i in mllist2:
        i['index'] = co
        co = co + 1
    data = {}
    data['ml'] = mllist
    data['mlli'] = mllist2
    data['dxid'] = dxid
    data['length'] = len(mllist2)
    data['type'] = type
    data['dxname'] = dxname
    data['sfid'] =  Daxue.objects.filter(id=dxid).all()[0].shengfen_id
    data['dxnum'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).count()
    data['wjname'] = wenjuan.objects.filter(id = tp)[0].wenjuan_name
    data['tp'] = tp
    return render_to_response('count/ml.html', data, RequestContext(req))


def xk(req):
    tp = req.GET.get("tp")
    dxid = req.GET.get("dxid")
    type = req.GET.get("type")
    mlid = req.GET.get("ml")
    dxname = Daxue.objects.filter(id=dxid).all()[0].daxue_name
    xklist = []
    xklist2 = []
    data = {}
    if type == '1':
        xk = Zyly.objects.filter(Zylx_id=mlid).all()
        mlname = Zylx.objects.filter(id=mlid).all()[0].Zylx_name
        data['mlname'] = mlname
        for i in xk:
            xke = {}
            xke['id'] = i.id
            xke['name'] = i.Zyly_name
            xke['num'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).filter(Jilu_xk=i.Zyly_name).count()
            temp = {}
            if xke['num'] != 0:
                temp["name"] = i.Zyly_name
                temp["num"] = xke['num']
                temp['index'] = len(xklist2) + 1
                xklist2.append(temp)
            xklist.append(xke)
    if type == '2':
        xk = Xsxk.objects.filter(Xsml_id=mlid).all()
        mlname = Xsml.objects.filter(id=mlid).all()[0].Xsml_name
        data['mlname'] = mlname
        for i in xk:
            xke = {}
            xke['id'] = i.id
            xke['name'] = i.Xsxk_name
            xke['num'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).filter(Jilu_xk=i.Xsxk_name).count()
            temp = {}
            if xke['num'] != 0:
                temp["name"] = i.Xsxk_name
                temp["num"] = xke['num']
                temp['index'] = len(xklist2) + 1
                xklist2.append(temp)
            xklist.append(xke)
    xklist2 = sorted(xklist2, key=operator.itemgetter('num'), reverse=True)
    co = 1
    for i in xklist2:
        i['index'] = co
        co = co + 1

    data['dxid'] = dxid
    data['type'] = type
    data['dxname'] = dxname
    data['length'] = len(xklist2)
    data['xk'] = xklist
    data['xkli'] = xklist2
    data['num'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).filter(Jilu_ml=data['mlname']).count()
    data['wjname'] = wenjuan.objects.filter(id = tp)[0].wenjuan_name
    data['tp'] = tp
    return render_to_response('count/xk.html', data, RequestContext(req))


def result(req):
    dxid = req.GET.get("dxid")
    type = req.GET.get("type")
    xkid = req.GET.get("ml")
    tp = req.GET.get("tp")
    dxname = Daxue.objects.filter(id=dxid).all()[0].daxue_name
    data = {}
    data['dxid'] = dxid
    data['type'] = type
    data['dxname'] = dxname
    data['tp'] = tp
    if type == '1':
        data['xkname'] = Zyly.objects.filter(id=xkid).all()[0].Zyly_name
        data['ml'] = Zyly.objects.filter(id=xkid).all()[0].Zylx_id
    if type == '2':
        data['xkname'] = Xsxk.objects.filter(id=xkid).all()[0].Xsxk_name
        data['ml'] = Xsxk.objects.filter(id=xkid).all()[0].Xsml_id
    data['num'] = Jilu.objects.filter(Jilu_tp=tp).filter(Jilu_daxue=dxname).filter(Jilu_xk=data['xkname']).count()
    data['wjname'] = wenjuan.objects.filter(id = tp)[0].wenjuan_name
    return render_to_response('count/result.html', data, RequestContext(req))


