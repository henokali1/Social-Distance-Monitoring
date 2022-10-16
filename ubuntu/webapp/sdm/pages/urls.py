from django.urls import path
from . import views
from .views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('report/', views.report, name='report.html'),
    path('get_ip/', views.get_ip, name='ip.html'),
    path('save_ip/', views.save_ip, name='tst.html'),
    path('ip/', views.ip, name='ip.html'),
]
