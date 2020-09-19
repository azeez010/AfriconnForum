from django.conf.urls import url
from django.urls import path
from . import views, resume

urlpatterns = [
    path('yourjobs/', views.yourjobs, name="yourjobs" ),
    path("resume/", views.resume, name="resume"),
    url(r'^create/$', views.create, name="create" ),
    url(r'^joblist/$', views.joblist, name="joblist" ),
    path('jobpage/', views.jobpage, name="jobpage" ),
    path('applicant/', views.eachJobs, name="eachJobs" ),
    path('make-resume/', resume.ViewPDF.as_view(), name="pdf_view"),
    path('show-resume/', views.show_resume, name="show-resume"),
    path('search-job/', views.search_job, name="search-job"),
    path('home/', views.home, name="job-home"),
    path('update-job/<int:pk>/', views.updateJobs.as_view(), name="update_job"),
    path('updateJob/<int:pk>/', views.update_job, name="update-job"),
]