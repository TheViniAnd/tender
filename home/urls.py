from django.conf.urls import url, include
from django.views.generic import DetailView
from django.conf import settings
from .models import Post
from . import views
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    url(r'^$', views.home_list, name='home_list'),
    url(r'^tender/new/', views.post_new, name='post_new'),
    url(r'^account/$', views.account, name = 'account'),
    path('account/tenderbuy/<int:pk>/', views.user_buy_tender, name = 'user_buy_tender'),
    url(r'^account/tenders/(?P<pk>\d+)/$', views.cash_new, name = 'cash_new'),
    url(r'^tender/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^tender/cash/', views.cash_new, name='cash_new'),
    url(r'^account/zaivki', views.view_tender, name='view_tender'),
    url(r'^register/$', views.RegisterFormView.as_view()),
    url(r'^login/$', views.LoginFormView.as_view()),
    url(r'^logout/$', views.LogoutView.as_view()),
]
if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)