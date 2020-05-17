from django.conf.urls import url
import views

urlpatterns = [
    url('^$', views.login, name='login'),
    url('^verifyCode$', views.verifyCode, name='verifyCode'),
    url('^login_handle$', views.login_handle, name='login_handle')
]