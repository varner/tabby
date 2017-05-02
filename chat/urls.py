from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sms/', views.sms, name='sms'),
    url(r'^enable-chaos/', views.enable_chaos, name='chaos'),
    #url(r'^collect/', views.collect, name='collect')
]