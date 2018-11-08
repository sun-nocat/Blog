from django.shortcuts import render
from django.http import *
# Create your views here.
from app import models
from app.models import User
import time
import datetime
import json
'''
return index.html
'''
def index(request):
    return render(request, 'index/index.html') #返回主页面

def home(request):
    return render(request,'home.html')  #返回文章发布页面

'''
文章上传接口
'''
def api_upload_article(request):
    if request.method == "POST":

        #判断用户是否登录,然后获取用户的姓名
        name = '孙明明 '

        title = request.POST.get('title',None)
        label = request.POST.get('label',None)
        content = request.POST.get('content',None)
        user = User.objects.get(name=name)

        models.Article.objects.create(
            time = datetime.datetime.now(),
            article_user_name = name,
            title = title,
            label = label,
            content = content,
            user = user
        )
        return HttpResponse('ok')


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
        article_list =  models.Article.objects.all().values_list('id','title') #只取id和title，形成一个列表
        lists = []
        for i in range(len(article_list)):
            obj = {}
            obj['id'] = article_list[i][0]
            obj['title'] = article_list[i][1]
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
        tel = request.POST.get('tel',None)
        email = request.POST.get('email',None)
        address = request.POST.get('address',None)
        status = 2 #账户权限，新用户默认为2
        if(account !=None and name != None):
            models.User.objects.create(
                account = account,
                name = name,
                tel = tel,
                email = email,
                address = address,
                status = status
            )
            print(User.objects.get(account=account))

            re = json.dumps({
                "status":"1",
                "mag":"注册成功",
                # "data":
            })
            response = HttpResponse(re,content_type="application/json,charset=utf8")
            response.set_cookie('')
            return
        else:
            return HttpResponse(json.dumps({"status":"0","msg":"注册失败"}),content_type="application/json,charset=utf8")
