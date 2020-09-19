from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('result/', views.result, name="result" ),
    url(r'^create/$', views.create, name="create" ),
    url(r'^new/$', views.new, name="new" ),
    path('poll/', views.poll, name="poll" ),
    path('vote/', views.vote, name='vote'),
    url(r'^results/$', views.results, name="results" ),
    path("search-poll/", views.search, name="search"),
    path("your-polls/", views.your_polls, name="your-polls")   
]