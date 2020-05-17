from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ordinary/(\d+)$', views.ordinary, name='ordinary'),
    url(r'^uqdate$', views.uqdate, name='uqdate'),
    url(r'^select_source/(\d+)$', views.select_source, name='select_source'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^select_xiangqing/(\d+)$', views.select_xiangqing, name='select_xiangqing'),
    url(r'sl_sname', views.sl_sname),
    url(r'^del$', views.delete),
    url(r'^cj_update$', views.cj_update)
]
