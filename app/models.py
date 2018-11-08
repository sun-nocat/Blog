from django.db import models

# Create your models here.

choice = (
    (1, '管理员'),
    (2, '用户'),
    (3, '游客')
)

'''
用户表
'''
class User(models.Model):
    id = models.AutoField(primary_key=True)  # 定义逐渐是Uid并自增
    account = models.CharField(max_length=20, null=False)  # 用户的账号
    name = models.CharField(max_length=20, null=False)  # 用户名
    password = models.CharField(max_length=15,default='') #密码
    tel = models.CharField(max_length=13,null=True)  # 用户的电话号码
    email = models.EmailField(max_length=20, null=True)  # 用户的邮箱
    address = models.CharField(max_length=30, null=True)  # 用户地址
    follow = models.CharField(max_length=5000,null=True) #关注列表
    status = models.IntegerField(choices=choice)  # 权限

    def __str__(self):
        return self.account


'''
文章表
'''

class Article(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(null=True)  # 文章创建时间
    article_user_name = models.CharField(max_length=20, null=True)  # 发布文章的作者名称
    title = models.CharField(max_length=20, null=False)  # 文章标题
    label = models.CharField(max_length=20, null=True)  # 文章标签
    content = models.TextField(default='')  # 文章内容
    commend = models.IntegerField(default=0)  # 收获的赞
    user = models.ForeignKey(User)  # 用户和文章关联

    def __str__(self):
        return self.title




'''
评论表
'''

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(null=True)  #发表评论时间
    content = models.CharField(max_length=500,null=False) #评论内容
    comment_user_name = models.CharField(max_length=20,null=False) #评论用户
    commend = models.IntegerField(default=0) #收获的赞
    article = models.ForeignKey(Article)  # 用户和文章互相关联

    def __str__(self):
        return self.comment_user_name

'''
文章图片地址表
'''

class ArticleImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images',null=False) #图片的相对于medio文件夹的地址
    image_name = models.CharField(max_length=500,null=False)
    width = models.CharField(max_length=10,null=True)
    height = models.CharField(max_length=10,null=True)
    status = models.CharField(max_length=10,null=True)

    def __str__(self):
        return self.image_name