from django.shortcuts import render, redirect
from .forms import create_blog
from .models import Blog
from forum.models import Favourite
from root.models import Advert
from django.utils import timezone
from django.contrib.auth.models import User 
from django.http import HttpResponse
from django.views.generic import UpdateView
import threading
from PIL import Image
import re
from django.db.models import Q
from django.contrib import messages
from os import path, remove
from django.core.paginator import Paginator
# below are for advert and adsmanager
from time import time
from random import randint
import json

# Create your views here.
def create(request):
    if request.user.is_authenticated:
        User_id = request.user.id
    
    #get the category through the id
    if request.method == "POST":
        # createBlog = create_blog(request.FILES, request.POST)
        blog = create_blog(request.POST, request.FILES)#, instance=Blog)
        if blog.is_valid():
            try:
                blogTitle = blog.cleaned_data['title']
                slugTitle = blogTitle.replace(" ", "-")
                blogPost = blog.cleaned_data['details']
                blogCategory = blog.cleaned_data['select_category']
                blogImage = blog.cleaned_data['image']
                blogTag = blog.cleaned_data['tags']
                blogs = Blog(user_id=User_id, title=blogTitle, tags=blogTag, slugTitle=slugTitle, details=blogPost, category=blogCategory, datetime=timezone.now(), image=blogImage)
                blogs.save()
                
                if blogImage:
                    blogObj = threading.Thread(target=blogResizeImg, args=[blogs.id])
                    blogObj.start()

            except Exception as e:
                print(e)
        
        messages.success(request, "blog created successfully")
        return redirect(f"/blog/your-blogs/")
    else:
        context = {"blog": create_blog}
        return render(request, "blog/create.html", context) 
    
def each_blog(request):
    slug = request.GET["title"]
    blog_id = request.GET["value"]
    getBlog = Blog.objects.get(slugTitle=slug, id=blog_id)
    getBlog.views += 1
    getBlog.save()
    blogTag = getBlog.tags
    pattern = blogTag.replace(" ", "|")
    read_time = len(getBlog.details) // 200
    recommend = Blog.objects.filter(~Q(id=blog_id), category=getBlog.category, tags__iregex=pattern)
    recommendation = recommend.order_by("views")[0:6]
    
    # I want to 2 ads in that category
    serialized_ad = ads_manager(getBlog.category, 2)

    fav = Favourite.objects.filter(fav_thread__iregex="/blog/", user_id=request.user.id, title=getBlog.title, fav_id=getBlog.id )
    fav_bool = True if len(fav) > 0 else False
   
    favAll = Favourite.objects.all()

    context = {"getBlog": getBlog, "serialized_ad": serialized_ad, "fav": favAll, "time": read_time, 'fav_bool': fav_bool,  "recommendation": recommendation}
    return render(request, "blog/eachBlog.html", context) 

# No ads here
def yourblog(request):
    getBlog = Blog.objects.filter(user_id=request.user.id)
    noPost = False
    if len(getBlog) < 1:
        noPost = True

    page = request.GET.get('page', 1)
    paginator = Paginator(getBlog, 2)
    
    try:
        Blogs = paginator.page(page)
    except PageNotAnInteger:
        Blogs = paginator.page(1)
    except Emptyage:
        Blogs = paginator.page(paginator.num_pages)
    
    context = {"getBlog": Blogs, "noPost": noPost}
    return render(request, "blog/yourblog.html", context) 

# Author's blog
def author(request):
    slug = request.GET["title"]
    blog_id = request.GET["value"]
    getBlog = Blog.objects.get(user_id=request.user.id, slugTitle=slug, id=blog_id)
    read_time = len(getBlog.details) // 200
    context = {"getBlog": getBlog, "time": read_time }
    return render(request, "blog/each_blog.html", context) 

class updateBlog(UpdateView):
    model = Blog
    template_name = 'blog/update_blog.html'
    form_class = create_blog

def update_blog(request, blog_id):
    if request.user.is_authenticated:
        User_id = request.user.id
    
    #get the category through the id
    if request.method == "POST":
        blogs = Blog.objects.get(user_id=User_id, id=blog_id) 
        blog = create_blog(request.POST, request.FILES)
        if User_id != blogs.user.id:
            messages.error(request, "you are not allow to edit this post")
            return redirect(f"/blog/authorUpdate/{{blogs.id}}/")
        
        if blog.is_valid():
            try:
                prevImage = blogs.image.path
                if path.exists(prevImage):
                    remove(blogs.image.path)
                
                
                blogTitle = blog.cleaned_data['title']
                slugTitle = blogTitle.replace(" ", "-")
                blogPost = blog.cleaned_data['details']
                blogCategory = blog.cleaned_data['select_category']
                blogImage = blog.cleaned_data['image']
                blogTag = blog.cleaned_data['tags']
                # update
                blogs.title=blogTitle 
                blogs.tags=blogTag
                blogs.slugTitle=slugTitle 
                blogs.details=blogPost
                blogs.category=blogCategory 
                blogs.datetime=timezone.now() 
                blogs.image=blogImage
                
                if blogImage:
                    blogObj = threading.Thread(target=blogResizeImg, args=[blogs.id])
                    blogObj.start()

                blogs.save()
            except Exception as e:
                print(e)
        
        messages.success(request, "blog is update successfully")
        return redirect(f"/blog/author-dashboard/{blogs.slugTitle}/{blogs.id}/")    

def blogResizeImg(ID):
    blog = Blog.objects.get(pk=ID)  
    img = Image.open(blog.image.path)
    if img.width > 300 or img.height > 300:
        imgsize = (350, 350)
        res = img.resize(imgsize)
        res.save(blog.image.path)
        img.close()

def delete(request, blog_id):
    if request.user.is_authenticated:
        User_id = request.user.id
        blogs = Blog.objects.filter(user_id=User_id, id=blog_id).first()
        
        if User_id != blogs.user_id:
            messages.error(request, "you re not allow to delete this post!")
            return redirect(f"/blog/author-dashboard/?title={blogs.slugTitle}&value={blogs.id}")
        else:    
            if blogs.image:
                prevImage = blogs.image.path
                if path.exists(prevImage):
                    remove(blogs.image.path)
                
                blogs.delete()
            else:
                blogs.delete()
            
            messages.success(request, "blog delete successfully")
            return redirect(f"/blog/your-blogs/")
    else:
        messages.error(request, "you hav to login to delete blog!")
        return redirect(f"/blog/author-dashboard/?title={blogs.slugTitle}&value={blogs.id}")

def home(request):
    trending = getBlog = Blog.objects.all().order_by("-bloglike")[0:6]
    getBlog = Blog.objects.all().order_by("-datetime")[0:6]
    
    fav = Favourite.objects.all() 
    context = {"getBlog": getBlog, "fav": fav, "trending": trending }
    return render(request, "blog/home.html", context) 

def search(request):
    if request.method == "POST":
        keyword = request.POST["search"]
        if keyword == "":
            messages.error(request, "enter something...")
            return redirect("/blog/search/")
        
        fav = Favourite.objects.all() 
        pattern = keyword.replace(" ", "|")
        blog = Blog.objects.filter(title__iregex=pattern)

        context = {"searches": blog, "fav": fav, "keyword":keyword}
        return render(request, "blog/searchBlog.html", context)
        
    return render(request, "blog/searchBlog.html")

def blogCategory(request, category):
    blog = Blog.objects.filter(category=category)
    fav = Favourite.objects.all() 

    
    # I want to 2 ads in that category
    serialized_ad = ads_manager(category, 2)

    page = request.GET.get('page', 1)
    paginator = Paginator(blog, 20)
    
    try:
        Blogs = paginator.page(page)
    except PageNotAnInteger:
        Blogs = paginator.page(1)
    except Emptyage:
        Blogs = paginator.page(paginator.num_pages)
    
    context = {"searches": Blogs, "category": category, "fav": fav,"serialized_ad": serialized_ad }
    return render(request, "blog/blogCategory.html", context)
    
def ads_manager(category, numba_of_ads):
    advert = Advert.objects.filter(advert_category=category, approved=True).values("advert_title", "advert_details", "advert_url", "advert")
    expiredAdvert = Advert.objects.filter(expiryDate__lte=time(), approved=True)
    
    # selecting advert through random process
    random_ads = len(advert) - numba_of_ads
    if random_ads < 0:
        random_ads = 0 
    
    start = randint(0, random_ads)
    end = start + numba_of_ads
    advert = advert[start:end]
    
    #this is not ideal it is to be change later
    for expired in expiredAdvert:
        send_messages = Messages(sender_id=1, msg=f"<p class='tweet-this'>Your ads has expired on {expired.ad_expirydatetime.strftime('%d %b %Y %I-%M%p')}</p>", receiver_id=expired.user_id, msg_type="ads expired", receiver_seen=False)
        send_messages.save() 
    
    expiredAdvert.delete()
    
    serialized_ad = []
    if len(advert) > 0:
        serialized_ad = advert
    
    return json.dumps(list(serialized_ad))
