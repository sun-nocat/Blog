#app.py/urls.pyy
from django.conf.urls import include, url
from app import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    url(r'^$', views.index), #
    url(r'^api/upload/article',views.api_upload_article), #文章上传
    url(r'^api/upload/image',views.api_upload_image),
    url(r'^home$',views.home),
    url(r'^get/articles$',views.get_article_list),
    url(r'^get/article$',views.get_article),
    url(r'^register$',views.register),
    url(r'^login$',views.login),
    url(r'^logout$',views.logout),
    url(r'^get/classList$', views.get_class_list),
    url(r'^get/articlesByClass$',views.get_article_list_by_class),
    url(r'^detail$',views.detail)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)