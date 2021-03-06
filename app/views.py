from django.shortcuts import render
from django.http import *
# Create your views here.
from app import models
from app.models import User
import time
import datetime
import json



'''
return index1.html
'''
def index(request):
    print(request.session.get('username'))
    print(request.session.get('account'))
    print(request.session.get('status'))
    print(request.session.get('id'))
    return render(request, 'index/index.html') #返回主页面

def loginPage(request):
    return render(request,'index/index1.html')

def home(request):
    if request.session.get('status'): #判断用户是否登录
        return render(request,'home.html')  #返回文章发布页面
    else:
        return HttpResponse('error')

'''
文章上传接口
参数：
title
label
content
'''
def api_upload_article(request):
    if request.method == "POST" and request.session.get('status'):

        #判断用户是否登录,然后获取用户的姓名
        title = request.POST.get('title',None)
        label = request.POST.get('label',None)
        content = request.POST.get('content',None)

        name = request.session.get('username')
        user = User.objects.get(id = request.session.get('id'))

        models.Article.objects.create(
            time = datetime.datetime.now(),
            article_user_name = name,
            title = title,
            label = label,
            content = content,
            user = user
        )
        re = json.dumps({
            "status":"1",
            "msg":"文章上传成功"
        })
        return HttpResponse(re,content_type="application/json;charset=utf-8")
    else:
        re = json.dumps({
            "status":"0",
            "mag":"文章上传失败"
        })
        return HttpResponse(re,content_type="application/json;charset=utf-8")

'''
文章图片上传的接口
'''
def api_upload_image(request):
    image = request.FILES.get('upload') #获取图片对象
    image_name = str(time.time())+ image.name  #获取图片的名称
    image.name = image_name
    # print(image.DEFAULT_CHUNK_SIZE)
    # print(image.read)
    models.ArticleImage.objects.create(
        image = image,
        image_name = image_name
    )
    url = '/media/images/' + image_name
    re = json.dumps({
        "uploaded":1,
        "url":url
    })
    return HttpResponse(re,content_type="application/json,charset=utf-8")



'''
获取所有文章的列表
返回值：文章id 和 文章的title
'''
def get_article_list(request):
    if request.method == "GET":
        article_list =  models.Article.objects.all().values_list('id','title','commend','time','article_user_name') #只取id和title，形成一个列表
        lists = []
        print((article_list[0][3]).strftime("%Y-%m-%d %H:%M:%S"))
        # print(datetime.datetime.strftime(""))


        for i in range(len(article_list)):
            obj = {}
            obj['id'] = article_list[i][0]
            obj['title'] = article_list[i][1]
            obj['commend'] = article_list[i][2]
            obj['time'] = (article_list[i][3]).strftime("%Y-%m-%d %H:%M:%S")
            obj['article_user_name'] = article_list[i][4]

            lists.append(obj)
        re = json.dumps({
            "status":"1",
            "data":lists
        })
        return HttpResponse(re,content_type="application/json,charset=utf8")

'''
根据文章的id获取文章的内容
'''
def get_article(request):
    id = request.GET.get('id',None)
    if id != None:
        article_list = models.Article.objects.filter(id=id)
        print(article_list)
        print(article_list[0].user)

        lists = []
        for i in range(len(article_list)):
            obj = {}
            obj['id'] = article_list[i].id
            obj['title'] = article_list[i].title
            obj['author'] = article_list[i].article_user_name
            obj['label'] = article_list[i].label
            obj['content'] = article_list[i].content
            obj['commend'] = article_list[i].commend
            lists.append(obj)
        re = json.dumps({
            "status":"1",
            "data":lists
        })
        return HttpResponse(re,content_type="application/json,charset=utf8")
    else:
        return HttpResponse("error")


'''
用户注册接口
参数
account
name
tel
email
address
'''
def register(request):
    if request.method == "POST":
        account = request.POST.get('account',None)
        name = request.POST.get('name',None)
        password = request.POST.get('password',None)
        tel = request.POST.get('tel',None)
        email = request.POST.get('email',None)
        address = request.POST.get('address',None)
        status = 2 #账户权限，新用户默认为2
        if(account != None and name != None and password != None):
            if models.User.objects.filter(account=account).exists():
                re = json.dumps({
                    "status":"0",
                    "msg":"账户已经存在"
                })
                return HttpResponse(re,content_type="application/json;charset=utf-8")
            else:
                models.User.objects.create(
                    account = account,
                    name = name,
                    password = password,
                    tel = tel,
                    email = email,
                    address = address,
                    status = status
                )
                # print(models.User.objects.filter(account=account).exists())
                ids = models.User.objects.filter(account=account)
                id = ids[0].id
                #将用户的信息保存在session中
                request.session['account'] = account
                request.session['name'] = name
                request.session['id'] = id
                request.session['status'] = status

                re = json.dumps({
                    "status":"1",
                    "mag":"注册成功"
                })
                response = HttpResponse(re,content_type="application/json;charset=utf-8")
                return response
        else:
            return HttpResponse(json.dumps({"status":"0","msg":"注册失败"}),content_type="application/json,charset=utf8")

'''
登录接口
参数
account
password
'''
def login(request):
    if request.method == "POST":
        account = request.POST.get('account',None)
        password = request.POST.get('password',None)
        user = models.User.objects.filter(account=account,password=password)
        print(user)
        # print(user[0].name)
        if user:
            #比较成功，登录成功,设置session
            request.session['account'] = account
            request.session['username'] = user[0].name
            request.session['status'] = user[0].status
            request.session['id'] = user[0].id
            re = json.dumps({
                "status":"1",
                "msg":"登录成功"
            })
            return HttpResponse(re,content_type="application/json;charset=utf-8")
        else:
            re = json.dumps({
                "status":"0",
                "msg":"用户名或密码错误"
            })
            return HttpResponse(re,content_type="application/json;charset=utf-8")

'''
清除session
'''
def logout(request):
    if request.session.get('status'):
        request.session.flush()  #清除所有session
        return HttpResponse(json.dumps({"status":"1","mag":"session清除完成"}),content_type="application/json;charset=utf-8")
    else:
        return HttpResponse(json.dumps({"status":"0","mag":"session清除失败"}),content_type="application/json;charset=utf-8")

'''
获取分类列表
返回分类的列表
'''
def get_class_list(request):
    class_list = models.Article.objects.values('label').distinct()
    print(class_list[0].get('label'))
    relist =[]
    for i in range(len(class_list)):
        relist.append(class_list[i].get('label'))
    re = json.dumps({
        "status":"1",
        "msg":"success",
        "data":relist
    })

    return HttpResponse(re,content_type="application/json;charset=utf-8")

'''
根据分类的标识找到相应的文章标题
'''

def get_article_list_by_class(request):
    if request.method == "GET":
        class_name = request.GET.get('label')
        article_list =  models.Article.objects.filter(label=class_name).values_list('id','title','commend','time','article_user_name') #只取id和title，形成一个列表
        print(len(list(article_list)))
        if len(list(article_list)) == 0:
            re = json.dumps({
                "status": "0",
                "data": ''
            })
            return HttpResponse(re, content_type="application/json,charset=utf8")
        lists = []
        print((article_list[0][3]).strftime("%Y-%m-%d %H:%M:%S"))

        for i in range(len(article_list)):
            obj = {}
            obj['id'] = article_list[i][0]
            obj['title'] = article_list[i][1]
            obj['commend'] = article_list[i][2]
            obj['time'] = (article_list[i][3]).strftime("%Y-%m-%d %H:%M:%S")
            obj['article_user_name'] = article_list[i][4]

            lists.append(obj)
        re = json.dumps({
            "status":"1",
            "data":lists
        })
        return HttpResponse(re,content_type="application/json,charset=utf8")

def detail(request):
    id = request.GET.get('id')
    request.COOKIES['id'] = id
    response = render(request,'index/detail.html')
    response.set_cookie('id',id)
    return response