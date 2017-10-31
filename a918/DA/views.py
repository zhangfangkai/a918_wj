# coding:utf-8
from django.shortcuts import render,render_to_response
from django.template.context import RequestContext
from models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import json
import csv
import pandas as pd
import copy
from collections import Counter
from RegressionTest import forward_selected


def login(req):
    if req.method == 'GET':
        return render_to_response('login.html', {}, RequestContext(req))
    else:
        username = req.POST.get('name')
        password = req.POST.get('password')
        if User.objects.filter(user_name=username, user_password=password).count() > 0:
            user_id = User.objects.filter(user_name=username)[0].id
            req.session['user_id'] = user_id
            data = {}
            try:
                data['user_name'] = username
                wenjuanlist = []
                for i in Wenjuan.objects.filter(user_id=user_id).all():
                    wenjuanlist.append(i.wj_name)
                data['wenjuanlist'] = wenjuanlist
            except Exception, e:
                print e
            return render_to_response('mainpage.html', data, RequestContext(req))
        else:
            return render_to_response('login.html', {}, RequestContext(req))

#----zfk modify on 2017-08-14
def mainpage(req):
    data = {}
    try:
        user_id = req.session['user_id']
        user = User.objects.get(pk=user_id)
        data['user_name'] = user.user_name
        wenjuanlist = []
        for i in Wenjuan.objects.filter(user_id=user_id).all():
            wj={}
            wj['id']=i.id
            wjcishu=Record.objects.filter(wenjuan_id=i.id).all()
            wj['wjtime']=i.wj_date
            wj['count']=wjcishu.count()
            wj['name']=i.wj_name
            wenjuanlist.append(wj)
        data['wenjuanlist'] = wenjuanlist
    except Exception, e:
        print e
    return render_to_response('mainpage1.html', data, RequestContext(req))

def wjmanage(req):
    data = {}
    try:
        user_id = req.session['user_id']
        user = User.objects.get(pk=user_id)
        data['user_name'] = user.user_name

        wenjuanlist = []
        for i in Wenjuan.objects.filter(user_id=user_id).all():
            wj={}
            wj['id']=i.id
            wjcishu = Record.objects.filter(wenjuan_id=i.id).all()
            wj['wjtime'] = i.wj_date
            wj['count'] = wjcishu.count()
            wj['name']=i.wj_name
            wenjuanlist.append(wj)
        data['wenjuanlist'] = wenjuanlist
    except Exception, e:
        print e
    return render_to_response('mainpage1.html', data, RequestContext(req))


def wjadd(req):
    data={}
    try:
        userid = req.session['user_id']
        name = req.GET.get('name')
        user = User.objects.get(pk= userid)
        #user.wenjuan_set.create(wj_name = name, wj_date =timezone.now())
        data['user'] = user
        data['wj_name'] = name
        data['id'] = userid
    except Exception, e:
        print e

    return render_to_response('wjadd.html',data,RequestContext(req))

def surveysave(req):
    surname=req.POST.get('svyName')
    surnote=req.POST.get('svyNote')
    userid = req.session['user_id']
    user = User.objects.get(pk=userid)

    # save wenjuan
    c=user.wenjuan_set.create(wj_name = surname, wj_date =timezone.now())
    a={}
    a["wjid"]=c.id

    return HttpResponse(json.dumps(a) ,content_type='application/json')

def optisave(req):
    userid=req.POST.get('belongId')
    wenjid = req.POST.get('wjid')
    wjid=Wenjuan.objects.get(id=wenjid)
    quid=req.POST.get('orderById')
    qutitle=req.POST.get('quTitle')
    quType=req.POST.get('quType')

    if quType == "RADIO":
        a = 1
    elif quType == 'CHECKBOX':
        a = 2
    elif quType == 'FILLBLANK':
        a = 3
    elif quType =='SCORE':
        a = 4
    elif quType == 'SCHOOL':
        a = 5
    elif quType == 'PROVINCE':
        a = 6
    elif quType == 'XUEWEI':
        a = 7
    else:
        a = quType

    qu = wjid.question_set.create(q_con=qutitle, questype_id=a, q_xuhao=quid)
    if a==1 or a==2 :
        i=0
        option = req.POST.get('optionValue_'+str(i))
        while(option):
            qu.choice_set.create(cho_num=i + 1, cho_con=option)
            i=i+1
            option = req.POST.get('optionValue_'+ str(i))
    elif a==4:
        i = 0
        option = req.POST.get('optionValue_' + str(i))
        while (option):
            qu.score_set.create(cho_num=i + 1, score_con =option)
            i = i + 1
            option = req.POST.get('optionValue_' + str(i))
    return render_to_response('mainpage1.html', {}, RequestContext(req))

def wjview(req):
    wenjuan_id = req.GET.get('wjid')
    wenjuan = Wenjuan.objects.filter(id=wenjuan_id)
    wenti = Question.objects.filter(wenjuan_id=wenjuan_id).all()

    if req.method == "GET":
        data = {}
        name= wenjuan.all()[0].wj_name
        data['wj_id']=wenjuan_id
        data['wj_name'] = name
        wj_data = []
        for i in wenti:
            wenti={}
            wenti_name = i.q_con
            wenti_type = i.questype_id
            wenti_id = i.id
            wenti_xuhao = i.q_xuhao
            wenti['wenti_name'] = wenti_name
            wenti['wenti_type'] = wenti_type
            wenti['wenti_xuhao'] = wenti_xuhao
            wenti['wenti_id'] = wenti_id
            xx = []
            if wenti_type == 1 or wenti_type == 2 :
                xuanxiang = Choice.objects.filter(question_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.cho_con
                    xuanxiang_xuhao = j.cho_num
                    xxx['xuanxiang_name']=xuanxiang_name
                    xxx['xuanxiang_xuhao']=xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            elif wenti_type == 4:
                xuanxiang = Score.objects.filter(question_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.score_con
                    xuanxiang_xuhao = j.cho_num
                    xxx['xuanxiang_name'] = xuanxiang_name
                    xxx['xuanxiang_xuhao'] = xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            wj_data.append(wenti)
        data['wj_data'] = wj_data
        return render_to_response('wjchakan.html', data, RequestContext(req))

def wjfabu(req):
    wenjuan_id = req.GET.get('wjid')
    wenjuan = Wenjuan.objects.filter(id=wenjuan_id)
    wenti = Question.objects.filter(wenjuan_id=wenjuan_id).all()
    if req.method == "GET":
        data = {}
        name= wenjuan.all()[0].wj_name
        data['wj_id']=wenjuan_id
        data['wj_name'] = name
        wj_data = []
        for i in wenti:
            wenti={}
            wenti_name = i.q_con
            wenti_type = i.questype_id
            wenti_id = i.id
            wenti_xuhao = i.q_xuhao
            wenti['wenti_name'] = wenti_name
            wenti['wenti_type'] = wenti_type
            wenti['wenti_xuhao'] = wenti_xuhao
            wenti['wenti_id'] = wenti_id
            xx = []
            if wenti_type == 1 or wenti_type == 2 :
                xuanxiang = Choice.objects.filter(question_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.cho_con
                    xuanxiang_xuhao = j.cho_num
                    xxx['xuanxiang_name']=xuanxiang_name
                    xxx['xuanxiang_xuhao']=xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            elif wenti_type == 4:
                xuanxiang = Score.objects.filter(question_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.score_con
                    xuanxiang_xuhao = j.cho_num
                    xxx['xuanxiang_name'] = xuanxiang_name
                    xxx['xuanxiang_xuhao'] = xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            wj_data.append(wenti)
        data['wj_data'] = wj_data
        return render_to_response('wjfabu.html', data, RequestContext(req))
    else:
        userid = req.session['user_id']
        wenjuan_id = req.POST.get('wjid')
        wenti = Question.objects.filter(wenjuan_id=wenjuan_id).all()
        if userid=='':
            aa=Record.objects.create(ans_data=timezone.now() , user_id=2,wenjuan_id=wenjuan_id)
        else:
            aa = Record.objects.create(ans_data=timezone.now(), user_id=userid, wenjuan_id=wenjuan_id)
        choiceobjs = []
        fillblanlobjs=[]
        scoreobjs=[]
        for i in range(1,wenti.count()+1):
            wenti_n=wenti.filter(q_xuhao=i).all()
            if wenti_n.first().questype_id==1 or wenti_n.first().questype_id==2:
                data=req.POST.getlist(str(i))
                for d in data:
                    obj={}
                    obj['huida_data']=d
                    choiceobjs.append(obj)
            elif wenti_n.first().questype_id == 3 or wenti_n.first().questype_id == 6 or wenti_n.first().questype_id == 7:
                data =req.POST.get(str(i))
                obj = {}
                obj['wenti_id'] = wenti_n.first().id
                obj['huida_data'] = data
                fillblanlobjs.append(obj)
            elif wenti_n.first().questype_id == 5:
                data=req.POST.get(str(i))
                obj={}
                obj['wenti_id'] =wenti_n.first().id
                templist=data.split(",")
                ee=City.objects.get(city_xuhao=templist[0])
                uni_id=University.objects.get(city_id=ee.id,univers_xuhao=templist[1])
                obj['huida_data'] = uni_id.id
                fillblanlobjs.append(obj)
            elif wenti_n.first().questype_id == 4:
                data = req.POST.getlist(str(i))
                i=1
                for d in data:
                    obj={}
                    bbb= Score.objects.filter(question_id = wenti_n.first().id, cho_num=i).all()
                    obj['xuanxiang_id']=bbb.first().id
                    obj['huida_data'] = d
                    scoreobjs.append(obj)
                    i+=1
        for i in choiceobjs:
            Ans_choice.objects.create(choice_id=i.get('huida_data'), record_id=aa.id)
        for i in fillblanlobjs:
            Ans_wenda.objects.create(question_id=i.get('wenti_id'),ans_con=i.get('huida_data'),record_id=aa.id)
        for i in scoreobjs:
            Ans_score.objects.create(score_id=i.get('xuanxiang_id'),scores=i.get('huida_data'),record_id=aa.id)

        return HttpResponse("Thank you for your answer!")
def wjdel(req):
    wenjuan_id = req.POST.get('wjid')
    wenjuan = Wenjuan.objects.filter(id=wenjuan_id)
    wenti = Question.objects.filter(wenjuan_id=wenjuan_id).all()
    for i in wenti:
        if i.questype_id==1 or i.questype_id==2:
            Choice.objects.filter(question_id=i.id).delete()
        elif  i.questype_id==4:
            Score.objects.filter(question_id=i.id).delete()
        i.delete()
    wenjuan.delete()
    data = {}
    data["wjid"]=wenjuan_id
    return HttpResponse(json.dumps(data), content_type='application/json')


def wjmodify(req):
    wenjuan_id = req.GET.get('wjid')
    print wenjuan_id
    wenjuan = Wenjuan.objects.filter(id=wenjuan_id)
    wenti = Question.objects.filter(wenjuan_id=wenjuan_id).all()

    if req.method == "GET":
        data = {}
        name = wenjuan.all()[0].wj_name
        data['wj_id'] = wenjuan_id
        data['wj_name'] = name
        wj_data = []
        for i in wenti:
            wenti = {}
            wenti_name = i.q_con
            wenti_type = i.questype_id
            wenti_id = i.id
            wenti_xuhao = i.q_xuhao
            wenti['wenti_name'] = wenti_name
            wenti['wenti_type'] = wenti_type
            wenti['wenti_xuhao'] = wenti_xuhao
            wenti['wenti_id'] = wenti_id
            xx = []
            if wenti_type == 1 or wenti_type == 2:
                xuanxiang = Choice.objects.filter(question_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.cho_con
                    xuanxiang_xuhao = j.cho_num
                    xxx['xuanxiang_name'] = xuanxiang_name
                    xxx['xuanxiang_xuhao'] = xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            elif wenti_type == 4:
                xuanxiang = Score.objects.filter(question_id=wenti_id).all()
                for j in xuanxiang:
                    xxx = {}
                    xuanxiang_name = j.score_con
                    xuanxiang_xuhao = j.cho_num
                    xxx['xuanxiang_name'] = xuanxiang_name
                    xxx['xuanxiang_xuhao'] = xuanxiang_xuhao
                    xxx['xuanxiang_id'] = j.id
                    xx.append(xxx)
                wenti['wenti_data'] = xx
            wj_data.append(wenti)
        data['wj_data'] = wj_data
        return render_to_response('wjmodify.html', data, RequestContext(req))

#----
#---- zyz add at 2017-09-03
def bgraph(req):
    data={}
    print "baiduecharts"
    return render_to_response('bgraph.html', data, RequestContext(req))


def make_zxt(req):
    data={}
    Quli="["
    gt = int(req.GET.get("gt"))
    print gt
    try:
        userid = req.session['user_id']
        wjlist={}

        for i in Wenjuan.objects.filter(user_id=userid).all():

            Quli = Quli + "{\"text\":\"" + i.wj_name + "\",\"nodes\":["
            for j in Question.objects.filter(wenjuan_id=i.id).all():
                idnum = str(j.id)
                if(j.questype_id != 3):
                    wjlist[idnum] = i.wj_name
                    if(j.questype_id == 4):
                        Quli = Quli + "{\"text\":\"" + j.q_con + "\",\"tags\":\"" + idnum + "\",\"nodes\":["
                        for k in Score.objects.filter(question_id=j.id).all():
                            Quli = Quli + "{\"text\":\"" + k.score_con + "\",\"tags\":\"" + idnum + "&" + str(k.id) +"\"},"
                        Quli = Quli[:-1]
                        Quli = Quli + "]},"
                    else:
                        Quli = Quli + "{\"text\":\"" + j.q_con + "\",\"tags\":\"" + idnum + "\"},"
            Quli = Quli[:-1]
            Quli = Quli + "]},"
        Quli = Quli[:-1]
        Quli = Quli + "]"
    except Exception, e:
        print e
    # data['choicedic'] = Quli.dumps(choicedic)
    # print Quli.dumps(choicedic)
    data['Quli'] = Quli
    result = json.dumps(wjlist, encoding='UTF-8', ensure_ascii=False)
    data['wjlist'] = result
    if gt == 1:
        return render_to_response('mkzxt.html', data, RequestContext(req))
    elif gt == 2:
        return render_to_response('mkqpt.html', data, RequestContext(req))
    elif gt == 3:
        return render_to_response('mkldt.html', data, RequestContext(req))
    elif gt == 4:
        return render_to_response('mkmap.html', data, RequestContext(req))
    else:
        return render_to_response('mkzxt.html', data, RequestContext(req))

def show_options(req):
    que_id = req.POST.get('qid')
    que_con = req.POST.get('qcon')
    wj_name = req.POST.get('wjname')

    data = {}
    cholist = {}
    options = "["
    idLi = []
    if(que_id.find("&") >= 0):
        idLi = que_id.split("&")
        qid = long(idLi[0])
    else:
        qid = long(que_id)

    try:
            qtype = Question.objects.get(id = qid).questype_id
            if (qtype == 6):
                for i in City.objects.all():
                    options = options + "{\"id\":\"" +que_id +"&"+ str(
                    i.city_xuhao) + "\"," +"\"type\":\""+str(qtype)+"\","+ "\"qcon\":\"" + que_con + "\"," + "\"wjname\":\"" + wj_name + "\"," + "\"con\":\"" + i.city_name + "\"},"
            elif(qtype == 5):
                for i in University.objects.all():
                    options = options + "{\"id\":\""  +que_id +"&"+ str(
                    i.univers_xuhao) + "\"," +"\"type\":\""+str(qtype)+"\","+ "\"qcon\":\"" + que_con + "\"," + "\"wjname\":\"" + wj_name + "\"," + "\"con\":\"" + i.univers_name + "\"},"
            elif(qtype == 4):
                if (len(idLi)>1):
                    for i in range(1,6,1):
                        options = options + "{\"id\":\""  +idLi[1] + "\",\"type\":\""+str(qtype)+"\","+ "\"qcon\":\"" + que_con + "\"," + "\"wjname\":\"" + wj_name + "\"," + "\"con\":\"" + str(i) + "\"},"
                else:
                    for i in Score.objects.filter(question_id=qid).all():
                        options = options + "{\"id\":\"" + str(i.id) + "\",\"type\":\"" + str(qtype) + "\"," + "\"qcon\":\"" + que_con + "\"," + "\"wjname\":\"" + wj_name + "\"," + "\"con\":\"" + i.score_con + "\"},"
            else:
                for i in Choice.objects.filter(question_id=qid).all():
                    options = options + "{\"id\":\"" + str(
                    i.id) + "\"," + "\"type\":\""+str(qtype)+"\","+"\"qcon\":\"" + que_con + "\"," + "\"wjname\":\"" + wj_name + "\"," + "\"con\":\"" + i.cho_con + "\"},"

            # cholist[i.id] = i.cho_con
    except Exception, e:
        print e
    options = options[:-1]
    options = options + "]"
    return JsonResponse(options, safe=False)


def submitvari(req):
    datagraph = {}
    idlist = req.POST.get(str(1))
    conlist = req.POST.get(str(2))
    typelist = req.POST.get(str(3))
    idlist = idlist[:-1]
    conlist = conlist[:-1]
    typelist = typelist[:-1]
    x_id = idlist.split(",")
    x_con = conlist.split(",")
    x_type = typelist.split(",")
    x_data = []

    idlist2 = req.POST.get(str(4))
    conlist2 = req.POST.get(str(5))
    typelist2 = req.POST.get(str(6))
    qidlist2 = req.POST.get(str(7))
    idlist2 = idlist2[:-1]
    conlist2 = conlist2[:-1]
    typelist2 = typelist2[:-1]
    qidlist2 =qidlist2[:-1]
    f_id = idlist2.split(",")
    f_con = conlist2.split(",")
    f_type = typelist2.split(",")
    f_qid = qidlist2.split(",")
    f_data = []

    con = "["

    for i in x_con:
        con = con + "\"" + i +"\","
    con = con[:-1]
    con = con + "]"

    if(len(idlist2) == 0):
        j = 0
        for i in x_type:
            xid = x_id[j]
            if (int(i) == 5 or int(i) == 6):
                idArray = xid.split("&")
                es = Ans_wenda.objects.filter(question_id=idArray[0], ans_con=idArray[1]).all()
                x_data.append(len(es))
            elif (int(i) == 4):
                # idArray = xid.split("&")
                es = Ans_score.objects.filter(score_id=xid,scores = int(x_con[j])).all()
                x_data.append(len(es))
            else:
                xid = int(xid)
                es = Ans_choice.objects.filter(choice_id=xid).all()
                x_data.append(len(es))
            j = j + 1
    else:
        filterlist={}
        j = 0
        for i in f_type:
            if(int(i) == 4):
                temp = Ans_score.objects.filter(scores=int(f_con[j]),score_id=int(f_id[j])).all()
                for k in temp:
                    if (filterlist.has_key(str(f_qid[j]))):
                        filterlist[str(f_qid[j])] = filterlist[str(f_qid[j])] + str(k.record_id) + ","
                    else:
                        filterlist[str(f_qid[j])] = str(k.record_id)
            elif(int(i) == 5 or int(i) == 6):
                temp = Ans_wenda.objects.filter(ans_con=f_id[j], question_id=int(f_qid[j])).all()
                for k in temp:
                    if (filterlist.has_key(str(f_qid[j]))):
                        filterlist[str(f_qid[j])] = filterlist[str(f_qid[j])] + str(k.record_id) +","
                    else:
                        filterlist[str(f_qid[j])] = str(k.record_id)
            else:
                temp = Ans_choice.objects.filter(choice_id=int(f_id[j])).all()
                for k in temp:
                    if (filterlist.has_key(str(f_qid[j]))):
                        filterlist[str(f_qid[j])] = filterlist[str(f_qid[j])] + "," + str(k.record_id)
                    else:
                        filterlist[str(f_qid[j])] = str(k.record_id)
            j = j + 1
        templist = []
        for i in filterlist:
            templist.extend(set(filterlist[i].split(",")))

        re_list = Counter(templist)
        max = len(filterlist)
        record = sorted(re_list.items(),key=lambda item:item[1],reverse=True)
        newrecord = []
        for j in record:
            if (j[1] == max):
                newrecord.append(int(j[0]))
            else:
                break
        j = 0
        for i in x_type:
            xid = x_id[j]
            if (int(i) == 5 or int(i) == 6):
                idArray = xid.split("&")
                es = Ans_wenda.objects.filter(question_id=idArray[0], ans_con=idArray[1]).all()
                num = 0
                for k in es:
                    if k.record_id in newrecord:
                        num = num + 1
                x_data.append(num)
            elif (int(i) == 4):
                # idArray = xid.split("&")
                es = Ans_score.objects.filter(score_id=xid,scores = int(x_con[j])).all()
                num = 0
                for k in es:
                    print k.record_id
                    if k.record_id in newrecord:
                        num = num + 1
                x_data.append(num)
            else:
                xid = int(xid)
                es = Ans_choice.objects.filter(choice_id=xid).all()
                num = 0
                for k in es:
                    if k.record_id in newrecord:
                        num = num + 1
                x_data.append(num)
            j = j + 1


    datagraph['data'] = json.dumps(x_data, encoding='UTF-8', ensure_ascii=False)
    datagraph['cate'] = con

    return render_to_response('zxt.html', datagraph, RequestContext(req))

#---- zyz 0903
def submitqpt(req):
    datagraph = {}
    idlist = req.POST.get(str(1))
    conlist = req.POST.get(str(2))
    typelist = req.POST.get(str(3))
    idlist = idlist[:-1]
    conlist = conlist[:-1]
    typelist = typelist[:-1]
    x_id = idlist.split(",")
    x_con = conlist.split(",")
    x_type = typelist.split(",")
    x_data = []

    idlist2 = req.POST.get(str(4))
    conlist2 = req.POST.get(str(5))
    typelist2 = req.POST.get(str(6))
    qidlist2 = req.POST.get(str(7))
    idlist2 = idlist2[:-1]
    conlist2 = conlist2[:-1]
    typelist2 = typelist2[:-1]
    qidlist2 = qidlist2[:-1]
    f_id = idlist2.split(",")
    f_con = conlist2.split(",")
    f_type = typelist2.split(",")
    f_qid = qidlist2.split(",")
    f_data = []

    filterlist = {}
    j = 0
    tempDic = {}
    numlist ={}
    for i in f_id:
        if( f_type[j] == '1' or f_type[j] == '2'):

            temp = Ans_choice.objects.filter(choice_id=int(i)).all()
            for k in temp:
                if (filterlist.has_key(str(i))):
                    filterlist[str(i)] = filterlist[str(i)] + "," + str(k.record_id)
                else:
                    filterlist[str(f_id[j])] = str(k.record_id)

            for k in x_id:
                es = Ans_score.objects.filter(score_id=k).all()
                ts =str(i)+"$"+str(k)
                tempDic[ts] = 0.0
                num = 0
                for p in es:
                    if (str(p.record_id) in filterlist[str(i)].split(",")):
                        num = num + 1
                        tempDic[ts] = tempDic[ts] + float(p.scores)
                tempDic[ts] = tempDic[ts] / num
                numlist[str(i)] = num
        elif( f_type[j] == '6' or f_type[j] == '5'):
            c = i.split("&")
            temp = Ans_wenda.objects.filter(ans_con=c[1],question_id=c[0]).all()
            for k in temp:
                if (filterlist.has_key(str(i))):
                    filterlist[str(i)] = filterlist[str(i)] + "," + str(k.record_id)
                else:
                    filterlist[str(i)] = str(k.record_id)

            for k in x_id:
                es = Ans_score.objects.filter(score_id=k).all()
                ts =str(i)+"$"+str(k)
                tempDic[ts] = 0.0
                num = 0
                for p in es:
                    if (str(p.record_id) in filterlist[str(i)].split(",")):
                        num = num + 1
                        tempDic[ts] = tempDic[ts] + float(p.scores)
                tempDic[ts] = tempDic[ts] / num
                numlist[str(i)] = num
        else:
            print "error"
        j = j + 1

    retDic = {}
    for i in tempDic.keys():
        a = i.split("$")
        if (retDic.has_key(a[0]) ):
            retDic[a[0]] = retDic[a[0]] +"," + str(tempDic[i])
        else:
            retDic[a[0]] = str(tempDic[i])

    datalist = []
    y = 0
    for i in retDic:
        temp = []

        c = retDic[i].split(",")
        temp.append(float(c[0]))
        temp.append(float(c[1]))
        temp.append(numlist[i])
        temp.append(f_con[y])
        temp.append("1")
        datalist.append(temp)
        y = y + 1

    datagraph['data'] = json.dumps(datalist,encoding='UTF-8', ensure_ascii=False)
    return render_to_response('qpt.html', datagraph, RequestContext(req))
#----

#---zfk add at 2017-08-31
def dataimp(req):
    try:
        xlsfile = r'D:\data\ceshi.csv'
        c = open(xlsfile,"rb")
        read = csv.reader(c)
        i = 0
        for line in read:
            i=i+1
            if i < 12:
                continue
            # aa = Record.objects.create(ans_data=timezone.now(), user_id=2, wenjuan_id=79)
            aa=38+i
            print str(i)+"----"+str(aa)
            # print len(line)
            for j in range(len(line)):
                if j< 2:
                    continue
                elif j > 2:
                    break
                else:
                    print line[j]
                    # # j== 14--20:
                    # q = Question.objects.get(wenjuan_id=79, q_xuhao=j-1)
                    # ch = Score.objects.get(question_id=227, cho_num=j-13)
                    # Ans_score.objects.create(scores=line[j],record_id=aa,score_id=ch.id)
                    Ans_wenda.objects.create(ans_con=line[j],question_id=255, record_id=aa)
            # if i>10:
            #     break
        c.close()
    except Exception, e:
        print e
    return HttpResponse('data import successful!')
#-----
#---zfk add at 2017-09-3
def ldt_data(req):
    idlist = req.POST.get(str(1))
    conlist = req.POST.get(str(2))
    typelist = req.POST.get(str(3))

    idlist = idlist[:-1]
    conlist = conlist[:-1]
    typelist = typelist[:-1]
    x_id = idlist.split(",")
    x_con = conlist.split(",")
    x_type = typelist.split(",")
    x_data = []

    idlist2 = req.POST.get(str(4))
    conlist2 = req.POST.get(str(5))
    typelist2 = req.POST.get(str(6))
    qidlist2 = req.POST.get(str(7))
    idlist2 = idlist2[:-1]
    conlist2 = conlist2[:-1]
    typelist2 = typelist2[:-1]
    qidlist2 = qidlist2[:-1]
    f_id = idlist2.split(",")
    f_con = conlist2.split(",")
    f_type = typelist2.split(",")
    f_qid = qidlist2.split(",")
    datagraph = {}

    con = "["

    for i in x_con:
        con = con + "{name:\"" + i + "\"," + "min:3,max:5}" + ","
    con = con[:-1]
    con = con + "]"

    j = 0
    Arecord = {}
    for i in f_type:
        if  int(i) == 5 or int(i) == 6:
            recordlist=[]
            x = f_id[j].split("&")
            temp = Ans_wenda.objects.filter(ans_con=x[1], question_id=int(f_qid[j])).all()
            for qq in temp:
                recordlist.append(qq.record_id)
            Arecord[j]=recordlist

        if  int(i) == 1 or int(i) == 2:
            recordlist = []
            temp = Ans_choice.objects.filter(choice_id=f_id[j]).all()
            for qq in temp:
                recordlist.append(qq.record_id)
            Arecord[j]=recordlist
        j = j + 1



    xuhao=0
    for xx in f_id:
        scorelist = []
        for ea in x_id:
            sumscore = 0
            num = 0
            singlescore = Ans_score.objects.filter(score_id=ea).all()
            for r in singlescore:
                if r.record_id in Arecord[xuhao]:
                    sumscore = sumscore + r.scores
                    num = num + 1
            jieguo = float(sumscore) / num
            scorelist.append(round(jieguo, 2))
        x_data.append(scorelist)
        xuhao=xuhao+1


    y_data = "["
    bb = 0
    for i in x_data:
        y_data = y_data + "{value:" + str(i) + ",name:\"" + f_con[bb] + "\"},"
        bb = bb + 1
    y_data = y_data[:-1]
    y_data = y_data + "]"

    y_name = "["
    for j in f_con:
        y_name = y_name + "\"" + j + "\","
    y_name = y_name[:-1]
    y_name = y_name + "]"

    datagraph['data'] = y_data
    datagraph['cate'] = con
    datagraph['name'] = y_name


    return render_to_response('ldt.html', datagraph, RequestContext(req))

#----- hbt add at 2017-9-3-------------


def basic_mainpage(req):
    data = {}
    try:
        user_id = req.session['user_id']
        user = User.objects.get(pk=user_id)
        data['user_name'] = user.user_name
        wenjuanlist = []
        for i in Wenjuan.objects.filter(user_id=user_id).all():
            xx = {}
            xx['name'] = i.wj_name
            xx['id'] = i.id
            wenjuanlist.append(xx)
        data['wenjuanlist'] = wenjuanlist
    except Exception, e:
        print e
    return render_to_response('basic_table.html', data, RequestContext(req))


def wenjuan_analyse(req):
    data = {}
    Quli = "["

    try:
        wj_id = req.GET.get('wj_id')
        req.session['wj_id'] = wj_id
        i = Wenjuan.objects.filter(id=wj_id)[0]
        Quli = Quli + "{\"text\":\"" + i.wj_name + "\",\"nodes\":["
        for j in Question.objects.filter(wenjuan_id=i.id).all():
            if j.questype_id != 3 and j.questype_id != 4:
                w_ques = []
                idnum = str(j.id)
                Quli = Quli + "{\"text\":\"" + j.q_con + "\",\"tags\":[\"" + idnum + "\"]},"
            elif j.questype_id == 4:
                Quli = Quli + "{\"text\":\"" + j.q_con + "\",\"nodes\":["
                for k in Score.objects.filter(question_id=j.id):
                    Quli = Quli + "{\"text\":\"" + k.score_con + "\",\"tags\":[\"" + str(j.id) + "," + str(k.id) + "\"]},"
                Quli = Quli[:-1]
                Quli = Quli + "]},"
        Quli = Quli[:-1]
        Quli = Quli + "]}"
        Quli = Quli + "]"
    except Exception, e:
        print e
    # data['choicedic'] = Quli.dumps(choicedic)
    # print Quli.dumps(choicedic)
    data['Quli'] = Quli
    return render_to_response('basic_analyse_varform.html', data, RequestContext(req))


def show_options_analyse(req):
    que_id = req.POST.get('qid')
    if ',' in que_id:
        que_id = que_id.split(',')
        qid = long(que_id[0])
        sc_id = que_id[1]
    else:
        qid = long(que_id)
    cholist = {}
    options = "["
    x = Question.objects.get(id=qid).questype_id
    if x == 5:
        try:
            for i in University.objects.all():
                options = options + "{\"id\":\"" + str(que_id) + 'u' + str(i.id) + "\",\"question\":\"" + Question.objects.get(
                    id=qid).q_con + "\",\"con\":\"" + i.univers_name + "\",\"del\":\"" + "X" + "\"},"
        except Exception, e:
            print e
    elif x == 6:
        try:
            for i in City.objects.all():
                options = options + "{\"id\":\"" + str(que_id) + 'p' + str(i.id) + "\",\"question\":\"" + Question.objects.get(
                    id=qid).q_con + "\",\"con\":\"" + i.city_name + "\",\"del\":\"" + "X" + "\"},"
        except Exception, e:
            print e
    elif x == 4:
        try:
            for l in range(1, 6):
                options = options + "{\"id\":\"" + str(sc_id) + 's' + str(
                    l) + "\",\"question\":\"" + Question.objects.get(
                    id=qid).q_con + ':  ' + Score.objects.get(id=sc_id).score_con + "\",\"con\":\"" + str(l) + "\",\"del\":\"" + "X" + "\"},"
        except Exception, e:
            print e
    else:
        try:
            for i in Choice.objects.filter(question_id=qid).all():
                options = options + "{\"id\":\"" + str(i.id) + "\",\"question\":\"" + Question.objects.get(
                    id=qid).q_con + "\",\"con\":\"" + i.cho_con + "\",\"del\":\"" + "X" + "\"},"
                # options = options + "{\"id\":\"" + str(i.id) + "\",\"con\":\"" + i.cho_con + "\"},"
                cholist[i.id] = i.cho_con
        except Exception, e:
            print e
    options = options[:-1]
    options = options + "]"
    return JsonResponse(options, safe=False)


def analyse_result(req):
    shaixuan = req.POST.get("shaixuan").split(',')
    varx_id = req.POST.get("x").split(',')
    vary_id = req.POST.get("y").split(',')[0]
    vary_id = vary_id.split('s')[0]
    shaixuan = shaixuan[:-1]
    varx_id = varx_id[:-1]
    wj_id = req.session.get("wj_id")
    varx = {}
    vary = []
    x_name = {}
    if shaixuan:
        shaixuan_id = {}
        count = 0

        for n in shaixuan:
            shai_list = []
            q_id = 0
            if 'p' in n:
                n = n.split('p')
                q_id = n[0]
                a = Ans_wenda.objects.filter(question_id=q_id, ans_con=n[1])
                if len(a):
                    for l in a:
                        shai_list.append(int(l.record_id))
            elif 'u' in n:
                n = n.split('u')
                q_id = n[0]
                a = Ans_wenda.objects.filter(question_id=q_id, ans_con=n[1])
                if len(a):
                    for l in a:
                        shai_list.append(int(l.record_id))
            elif 's' in n:
                n = n.split('s')
                q_id = Score.objects.get(score_id=n[0]).question_id
                a = Ans_score.objects.filter(score_id=n[0], scores=n[1])
                if len(a):
                    for l in a:
                        shai_list.append(int(l.record_id))
            else:
                n = int(n)
                q_id = Choice.objects.get(id=n).question_id
                a = Ans_choice.objects.filter(choice_id=n)
                if len(a):
                    for l in a:
                        shai_list.append(int(l.record_id))
            if shaixuan_id.has_key(str(q_id)):
                shaixuan_id[str(q_id)] = list(set(shaixuan_id[str(q_id)]) | (set(shai_list)))
            else:
                shaixuan_id[str(q_id)] = shai_list
                count += 1
        shai_list = []
        for k,v in shaixuan_id.items():
            shai_list.extend(v)
        dict1 = Counter(shai_list)
        record = sorted(dict1.items(), key=lambda item:item[1], reverse=True)
        i = 0
        record_id = []
        while record[i][1] == count:
            record_id.append(record[i][0])
            i += 1
            if i == len(record):
                break

        for l in record_id:
            vary.append(int(Ans_score.objects.get(record_id=l, score_id=vary_id).scores))

        x_num = 1
        for m in varx_id:
            m = m.split('s')[0]
            m = int(m)
            x_list = []
            if 'x'+str(x_num) in varx.keys():
                continue
            else:
                for l in record_id:
                    x_list.append(int(Ans_score.objects.get(record_id=l, score_id=m).scores))
                varx['x' + str(x_num)] = x_list
                x_name['x' + str(x_num)] = Score.objects.get(id=m).score_con
                x_num += 1

    else:
        a = Ans_score.objects.filter(score_id=vary_id)
        if len(a):
            for l in a:
                vary.append(int(l.scores))
        x_num = 1
        for m in varx_id:
            m = m.split('s')[0]
            m = int(m)
            x_list = []
            if 'x'+str(x_num) in varx.keys():
                continue
            else:
                a = Ans_score.objects.filter(score_id=m)
                if len(a):
                    for l in a:
                        x_list.append(int(l.scores))
                    varx['x' + str(x_num)] = x_list
                    x_name['x' + str(x_num)] = Score.objects.get(id=m).score_con
                    x_num += 1


    var = copy.deepcopy(varx)
    y_name = Score.objects.get(id=vary_id).score_con
    var['y'] = vary

    data = {}
    data1 = pd.DataFrame(var)
    model = forward_selected(data1, 'y')
    modelhat = model.summary().as_html().replace('simpletable', 'table')
    modelbar = modelhat.split(r'</table>')
    data['regression1'] = modelbar[0] + r'</table>'
    data['regression2'] = modelbar[1] + r'</table>'
    data['regression3'] = modelbar[2] + r'</table>'
    data['y'] = y_name
    data['x'] = x_name
    return render_to_response('analyse_result.html', data, RequestContext(req))


def submit_map(req):
    data = {}
    idlist = req.POST.get(str(1))
    conlist = req.POST.get(str(2))
    typelist = req.POST.get(str(3))
    idlist = idlist[:-1]
    conlist = conlist[:-1]
    typelist = typelist[:-1]
    x_id = idlist.split(",")
    x_con = conlist.split(",")
    x_type = typelist.split(",")
    x_data = {}
    que_id = Choice.objects.get(id=x_id[0]).question_id
    title = Question.objects.get(id=que_id).q_con
    wj_id = Question.objects.get(id=que_id).wenjuan_id
    que_id = Question.objects.get(wenjuan_id=wj_id, questype=6).id
    max_num = 0
    for y in x_id:
        i = 0
        if int(x_type[i]) == 1 or int(x_type[i]) == 2:
            province_data = {}
            for x in City.objects.all():
                if x.id != 70:
                    m = Ans_choice.objects.filter(choice_id=int(y))
                    n = Ans_wenda.objects.filter(question_id=que_id, ans_con=x.city_xuhao)
                    set_m = set()
                    set_n = set()
                    for p in m:
                        set_m.add(p.record_id)
                    for q in n:
                        set_n.add(q.record_id)
                    l = set_m & set_n
                    name = x.city_name.replace(u"市", "")
                    name = name.replace(u"省", "")
                    name = name.replace(u'自治区', '')
                    name = name.replace(u'特别行政区', '')
                    name = name.replace(u'壮族', '')
                    name = name.replace(u'回族', '')
                    name = name.replace(u'维吾尔', '')
                    province_data[name] = len(l)
                    if province_data[name] > max_num:
                        max_num = province_data[name]
            x_data[Choice.objects.get(id=int(y)).cho_con] = province_data
            i += 1
    data['title'] = '\"' + title + '\"'
    list1 = '['
    for k in x_id:
        list1 = list1 + '\"' + Choice.objects.get(id=k).cho_con + '\",'
    list1 = list1[:-1]
    list1 = list1 + ']'
    data['choice'] = list1
    data['x_data'] = x_data
    data['max_num'] = max_num
    # for o in x_data:
    #     print o
    #     for p in x_data[o]:
    #         print p
    #         print x_data[o][p]
    return render_to_response('map.html', data, RequestContext(req))