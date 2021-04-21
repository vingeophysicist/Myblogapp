from django.contrib import admin
from django.urls import path, include, re_path
from . import views







app_name = 'blog'


urlpatterns = [
    path('', views.index, name ='indexpage'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/',
        views.post_detail,
        name ='post_detail'),
    path('tag/<slug:slug>/', views.tagged, name = 'tagged'),
    path('<slug:category_slug>/', views.category_detail_views, name = 'category_detail_views'),
    re_path(r'^subscribe/', views.subscribe, name = 'subscribe'),
    path('about.html/',views.aboutme, name = 'aboutme'),
    path('contact.html/', views.contact, name = 'contact'),
   

]





