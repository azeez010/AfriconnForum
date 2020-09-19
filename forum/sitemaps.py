from django.contrib.sitemaps import Sitemap
from root.models import Profile
from polls.models import Poll
from job.models import Job
from blog.models import Blog
from .models import Thread, Category
from django.shortcuts import reverse

class StaticViewSiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return ['search-blog', 'forum-home', 'blog-home', 'all-category', 'search-forum', 'register', 'login', 'home', 'countrystats', 'info', 'new', 'search', 'results', "job-home", 'search-job', 'joblist']
    def location(self, item):
        return reverse(item)

class ProfileSiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return Profile.objects.all()
    
class PollSiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return Poll.objects.all()
    
class CategorySiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return Category.objects.all()

class ThreadSiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return Thread.objects.all()

class JobSiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return Job.objects.all()

class BlogSiteMap(Sitemap):
    changeFreq = 'always'
    def items(self):
        return Blog.objects.all()
