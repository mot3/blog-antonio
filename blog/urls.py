from django.urls import path
from . import views

# URL patterns allow you to map URLs to views

# Define an application namespace, This allows you to organize URLs by application
app_name = 'blog'

urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
]
