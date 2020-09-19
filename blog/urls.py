from django.conf.urls import url
from django.urls import path
from . import views
from . import functionalities
from .views import updateBlog 

urlpatterns = [
    path('each/', views.each_blog, name="each_blog"),
    path('your-blogs/', views.yourblog, name="your-blog"),
    path('like/', functionalities.likes, name="blog_like"),
    path('author-dashboard/', views.author, name="blog_author"),
    path('author-update/<int:pk>/', updateBlog.as_view(), name="blog_update"),
    path('authorUpdate/<int:blog_id>/', views.update_blog, name="blog-update"),
    path('author-delete/<int:blog_id>/', views.delete , name="blog_delete"),
    url(r'^create', views.create, name="create"),
    path('home/', views.home, name="blog-home"),
    path('search/', views.search, name="search-blog"),
    path("categories/<str:category>/", views.blogCategory, name="blogCategory"),
   
]