from django.shortcuts import render, redirect
from django.http import HttpResponse 
from .forms import ProfileForm, UserForm
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User 
from os import path, remove
from PIL import Image
import threading
from forum.models import Report, ReportThread, Category, Thread, Comment, Favourite, Share, Category, CountryStats, OnlineUser, Members
from polls.models import Poll
from blog.models import Blog
from job.models import Job
from django.views.generic import DetailView, UpdateView
from .models import Profile, Messages, Ban, TransactionType, Advert, Following
from datetime import timedelta, datetime
from time import time
from itertools import chain
from operator import itemgetter
from django.core.paginator import Paginator
from django.core import serializers
from django.contrib.auth import authenticate, login
from django.contrib.gis.geoip2 import GeoIP2
from math import ceil
from django.core.mail import send_mail
from forum.views import ads_manager
import json   
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Info contain a html that has About and Terms of Use
def info(request):
    return render(request, "root/info.html")


def home(request):
    return redirect("/forum/home/")

def profile(request):
    no_of_threads = Thread.objects.all().count() 
    user = User.objects.get(pk=request.user.id)
    
    all_user = User.objects.all().count()
    # online and offline users
    online_user_threshold = round(time() - 60)
    guest_users = OnlineUser.objects.filter(is_authenticated=False, last_seen__gte=online_user_threshold).count()
    logined_users = OnlineUser.objects.filter(is_authenticated=True, last_seen__gte=online_user_threshold).count()
    
    image = ProfileForm()
    form = UserForm()
    context = {"img": image, "form": form, "guest_users" : guest_users, "logined_users": logined_users, "all_users": all_user, "user": user,"no_of_threads":no_of_threads }
    return render(request, "root/profile.html", context)

def visit_profile(request, username):
    user_profile = User.objects.get(username=username)
    all_follower = Following.objects.filter(following=user_profile.id)
    following = Following.objects.filter(following_id=user_profile.id, follower_id=request.user.id, followBool=True)
    context = {"object": user_profile, "all_follower": all_follower.count() }
    if len(following) > 0:
        context = {"object": user_profile,"all_follower": all_follower.count(), "following": following}    
    return render(request, "root/user_profile.html", context)


class updateProfile(UpdateView):
    model = Profile
    template_name = 'root/edit_profile.html'
    form_class = ProfileForm

def update_profile(request):
    if request.method == "POST":
        redirect_url = request.POST["redirect"]  
        if redirect_url == "":
            redirect_url = '/profile/'  


        profile = Profile.objects.get(user_id=request.user.id)
        image = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if image.is_valid():
            save_location = image.save(commit=False)
            # try to update profile's location
            user_location = GeoIP2()
            try:
                x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

                if x_forwarded_for:
                    ip = x_forwarded_for.split(',')[0]
                else:
                    ip = request.META.get('REMOTE_ADDR')

                user_city = user_location.city(ip)
                save_location.city = user_city['city']
                save_location.country = user_city["country_code3"]
                if save_location.profile_pic:
                    im = Image.open(save_location.profile_pic)
                    output = BytesIO()
                    # Resize/modify the image
                    im = im.resize((200, 200))
                    # after modifications, save it to the output
                    im.save(output, format='PNG', quality=90)
                    output.seek(0)
                    # change the imagefield value to be the newley modifed image value
                    save_location.profile_pic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % save_location.profile_pic.name.split('.')[0], 'image/jpeg',
                                                    sys.getsizeof(output), None)
                    save_location.save()

                all_countrymen = Profile.objects.filter(country=user_country["country_code"]).count()
                country, create = CountryStats.objects.get_or_create(country=user_country["country_code"], defaults={"no_of_user": "0"})
                country.no_of_user = all_countrymen
                country.save()            
            except Exception as error:
                if save_location.profile_pic:
                    im = Image.open(save_location.profile_pic)
                    output = BytesIO()
                    # Resize/modify the image
                    im = im.resize((200, 200))
                    # after modifications, save it to the output
                    im.save(output, format='PNG', quality=80)
                    output.seek(0)
                    # change the imagefield value to be the newley modifed image value
                    save_location.profile_pic = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % save_location.profile_pic.name.split('.')[0], 'image/jpeg',
                                                    sys.getsizeof(output), None)
                save_location.save()
                print(f"{error} an error occured while trying to update user's location")

            messages.success(request, f"{profile.user.username}, you profile is sucessfully updated")
            return redirect(f'{redirect_url}')

def transfer(request):
    if request.user.is_authenticated:
        user_id = request.user.id
    
    to = request.POST["to"]
    points = request.POST["points"]
    to_user = User.objects.filter(username=to.lower())
    from_user = User.objects.get(id=user_id)

    if to == request.user.username:
        messages.error(request, f"You can't transfer points to yourself")
        return redirect('/profile/')
    
    if len(to_user) == 0:
        messages.error(request, f"there is no such user as {to}")
        return redirect('/profile/')
    
    toId = to_user.first().id
    toUser = Profile.objects.get(user_id=toId)
    fromUser = Profile.objects.get(user_id=from_user.id)
    
    if fromUser.afrika_deeds < int(points):
        messages.error(request, f"there is not enough funds to send to {to}")
        return redirect('/profile/')
        
        
    toUser.afrika_deeds += int(points)
    fromUser.afrika_deeds -= int(points)
    
    msg = f"{fromUser.user.username}, sent you {points} afrikaz deeds"
    send_messages = Messages(sender_id=fromUser.user_id, msg=msg, receiver_id=toUser.user_id, msg_type="transfer points", receiver_seen=False)
    send_messages.save()
    toUser.save() 
    fromUser.save()

    messages.success(request, f"you successfully transfer points to {to}")
    return redirect('/profile/')

def report(request, obj_type, obj_id):
    if request.user.is_superuser:
        if obj_type == "thread":
            thread = Thread.objects.filter(id=obj_id).first()
            context = { "object": thread, "type": obj_type }
            return render(request, "root/each_report.html", context)  
        elif obj_type == "comment":    
            comment = Comment.objects.filter(id=obj_id).first()
            context = { "object": comment, "type": obj_type }
            return render(request, "root/each_report.html", context)
    else:
        messages.error(request, "you are not allowed to access that page")
        return redirect("/profile/")    


def report_seen(request, obj_type, obj_id):
    if request.user.is_superuser:
        if obj_type == "thread":
            report_thread = ReportThread.objects.filter(thread_id=obj_id).first()
            report_thread.delete()
            messages.success(request, "report viewed successfully")
            return redirect("/profile/report/")
          
        elif obj_type == "comment":    
            report_comment = Report.objects.filter(comment_id=obj_id).first()
            report_comment.delete()
            messages.success(request, "report viewed successfully")
            return redirect("/profile/report/")
    else:
        messages.error(request, "you are not allowed to access that page")
        return redirect("/profile/")    

def report_ban(request, user_id, obj_type, obj_id):
    if request.user.is_superuser:
        check_ban = Ban.objects.filter(user_id=user_id)
        user = User(id=user_id)
        if obj_type == "thread":
            if len(check_ban) == 0:
                #setting an expiry date
                expiryTime = time() + int("86400")
                #banning the user
                ban = Ban(user_id=user_id, expiry_time = expiryTime, on_ban = True )
                ban.save()
                # deleting the report
                report_thread = ReportThread.objects.filter(thread_id=obj_id).first()
                report_thread.delete()
                #messaging the banned user
                msg = f"{report_thread.thread.user.username}, you have been banned for a day"
                send_messages = Messages(sender_id=request.user.id, msg=msg, receiver_id=user.id, msg_type="ban", receiver_seen=False)
                send_messages.save()
                
                messages.success(request, f"{report_thread.thread.user.username} banned successfully for a day")
                return redirect("/profile/")
            else:
                #setting an expiry date
                expiryTime = time() + int("86400")
                #banning the user
                check_ban.first().expiry_time = expiryTime
                check_ban.first().on_ban = True
                check_ban.first().save()
                # deleting the report
                report_thread = ReportThread.objects.filter(thread_id=obj_id).first()
                report_thread.delete()
                #messaging the banned user
                msg = f"{report_thread.thread.user.username}, you have been banned for a day"
                send_messages = Messages(sender_id=request.user.id, msg=msg, receiver_id=user.id, msg_type="ban", receiver_seen=False)
                send_messages.save()
                

                messages.success(request, f"{report_thread.thread.user.username} banned successfully for a day")
                return redirect("/profile/")

        elif obj_type == "comment":    
            if len(check_ban) == 0:
                expiryTime = time() + int("86400")
                ban = Ban(user_id=user_id, expiry_time = expiryTime, on_ban = True )
                ban.save()
                # deleting the report
                report_comment = Report.objects.filter(comment_id=obj_id).first()
                report_comment.delete()
                # send message to the banned user
                msg = f"{report_comment.comment.user.username}, you have been banned for a day"
                send_messages = Messages(sender_id=request.user.id, msg=msg, receiver_id=user.id, msg_type="ban", receiver_seen=False)
                send_messages.save()
                
                messages.success(request, f"{report_comment.comment.user.username} banned successfully for a day")
                return redirect("/profile/")
            else:
                expiryTime = time() + int("86400")
                check_ban.first().expiry_time = expiryTime
                check_ban.first().on_ban = True
                check_ban.first().save()
                # deleting the report
                report_comment = Report.objects.filter(comment_id=obj_id).first()
                report_comment.delete()
                #messaging the banned user
                msg = f"{report_comment.comment.user.username}, you have been banned for a day"
                send_messages = Messages(sender_id=request.user.id, msg=msg, receiver_id=user.id, msg_type="ban", receiver_seen=False)
                send_messages.save()
                
                messages.success(request, f"{report_comment.comment.user.username} banned successfully for a day")
                return redirect("/profile/")
        
    else:
        messages.error(request, "you are not allowed to access that page")
        return redirect("/profile/")    

def transactions(request):
    if request.user.is_superuser:
        cost = request.POST["cost"]
        category = request.POST["category"]
        
        check = TransactionType.objects.filter(activity=category)
        if len(check) > 0:
            first = check.first()
            first.cost = cost
            first.save() 
            messages.success(request, f"{request.user.username}, {first.activity} Category has been updated  ")
            return redirect("/profile/")
        else:    
            transaction_type = TransactionType(activity=category, cost=cost)
            transaction_type.save()
            
            messages.success(request, f"{request.user.username}, {transaction_type.activity} Category has been set for transaction")
            return redirect("/profile/")
    else:
        messages.error(request, f"{request.user.username}, You are not allowed to set category for advertisement  ")
        return redirect("/profile/")
    
def advertisement(request):
    if request.method == "POST":
        country = request.POST["country"]
        advert = request.FILES["advert_pic"]
        advert_url = request.POST["advert_url"]
        advert_title = request.POST["advert_title"]
        advert_time = request.POST["time"]
        details = request.POST["details"]
        ad_type = request.POST["ad_type"]
        # for country specific ads
        countryData = country.split(" ")
        countryName = countryData[0]
        if countryName == "all":
            total_users = 1
            allUsers = int(countryData[1])
        else:    
            countryNoOfUsers = countryData[1]
            allUsers = int(countryData[2])
            total_users = int(countryNoOfUsers) / int(allUsers)
        # ad time
        days = int(advert_time) / 86400
        
        if ad_type == "all":
            all_web = TransactionType.objects.get(activity="all")
            cost = all_web.cost * days * total_users
            total_cost = ceil(cost)
            
        elif ad_type == "feeds":
            feeds = TransactionType.objects.get(activity="feeds")
            cost = feeds.cost * days * total_users
            total_cost = ceil(cost)

        elif ad_type == "home":
            home = TransactionType.objects.get(activity="home")
            cost = home.cost * days * total_users
            total_cost = ceil(cost)
            
        elif ad_type == "hamlet":
            option = request.POST["option"]
            hamlet_details = option.split(",")
            category_title = hamlet_details[0]
            # set ads type to hamlet title
            ad_type = category_title 
            no_of_user = hamlet_details[1]
            no_of_member = hamlet_details[2]
            ad_rate = TransactionType.objects.get(activity="ad_rate")
            cost = int(no_of_member) * int(no_of_user) * ad_rate.cost * days * total_users
            total_cost = ceil(cost)

        
        userProfile = Profile.objects.get(user_id=request.user.id)
        user_ADs = userProfile.afrika_deeds
        
        if user_ADs < total_cost:
            messages.error(request, f"{request.user.username}, you don't have enough ADSs, you can earn them through referrals and being liked for now")
            return redirect("/advertisement/")
        else:    
            advert = Advert(advert=advert, advert_title=advert_title, advert_url=advert_url, advert_details=details, ad_country=countryName, advert_category=ad_type, expiryDate=int(advert_time), user_id = request.user.id, cost=int(total_cost)) 
            userProfile.afrika_deeds -= total_cost
            send_messages = Messages(sender_id=1, msg=f"<p>Your ads has created and it is pending for admin's approval, Thank for placing an ad with us</p>", receiver_id=advert.user_id, msg_type="ads place successfully", receiver_seen=False)
            send_messages.save()

            send_messages = Messages(sender_id=userProfile.user_id, msg=f"<p>An ads has been placed by user {userProfile.user.username} <a class='tweet-this'href='/ads-approval/'>approve</a></p>", receiver_id=1, msg_type="ads place successfully", receiver_seen=False)
            send_messages.save()
            
            userProfile.save()
            advert.save()
            # Save url for javascript
            if advert.advert:
                advert.advert_image_url = advert.advert.url
                advert.save() 
            subject = f"{userProfile.user.username} placed an adverts on Africonn"
            message = f"A mail was place by {userProfile.user.username} on {datetime.now()}. As the admin it is your responsible to approve the Ads so that it can be displayed to other users. Visit http://www.africonn.com with your admin login details to be able to approve the advert"
            # notify the with an e-mail
            try:
                send_mail(subject=subject, from_email="dataslid@gmail.com", message=message,recipient_list=["dataslid@gmail.com"], fail_silently=True )
            except Exception:
                print(f"something went wrong {Exception}")
                
            messages.success(request, f"{request.user.username}, you have placed an advert successfully")
            return redirect("/advertisement/")
    else:
        all_categories = Category.objects.all()
        feeds = TransactionType.objects.get(activity="feeds")
        home = TransactionType.objects.get(activity="home")
        all = TransactionType.objects.get(activity="all")
        ad_rate = TransactionType.objects.get(activity="ad_rate")
        countrystats = CountryStats.objects.all()
        no_of_users = User.objects.all()
        you = User.objects.get(id=request.user.id)
        categories = f"{serializers.serialize('json', all_categories)}"
        
        context = {"all_categories": categories, "you": you, 'no_of_users': no_of_users.count(), "ad_rate": ad_rate, "countrystats": countrystats, "all": all, "feeds": feeds, "home": home }
        return render(request, "forum/advertisement.html", context)

def your_ads(request):
    advert = Advert.objects.filter(user_id=request.user.id)
    context = {"advert": advert}
    return render(request, "root/your_ads.html", context)

def ads_approval(request):
    if request.method == "POST":
        option = request.POST["option"]
        advert = request.FILES["advert_pic"]
        advert_url = request.POST["advert_url"]
        advert_time = request.POST["time"]
        details = request.POST["details"]
        
        data = option.split(" ")
        
        if len(data) < 2:
            messages.error(request, f"{request.user.username}, select a category")
            return redirect("/advertisement/")
            
        category = data[0]
        cost = data[1]
        days = int(advert_time) / 86400
        
        total_cost = int(cost) * days
        
        user = Profile.objects.get(user_id=request.user.id)
        user_ADs = user.afrika_deeds
        
        if user_ADs < total_cost:
            messages.error(request, f"{request.user.username}, you don't have enough ADSs, you can earn them through referrals and being liked for now")
            return redirect("/advertisement/")
        else:    
            advert = Advert(advert=advert, advert_url=advert_url, advert_details=details, advert_category=category, expiryDate=int(advert_time) + int(time()), user_id = request.user.id, cost=int(total_cost)) 
            user.afrika_deeds -= total_cost
            user.save()
            advert.save()
            messages.success(request, f"{request.user.username}, you have placed an advert successfully")
            return redirect("/advertisement/")
    else:
        adverts = Advert.objects.filter(approved=False)
        hasPost = False
        if adverts.count() < 1:
            hasPost = True
        

        page = request.GET.get('page', 1)
        paginator = Paginator(adverts, 20)
        try:
            ads = paginator.page(page)
        except PageNotAnInteger:
            ads = paginator.page(1)
        except Emptyage:
            ads = paginator.page(paginator.num_pages)

        context = {"ads": ads}
        return render(request, "root/ad_approval.html", context)


def follower_page(request):
    following = Following.objects.filter(follower_id=request.user.id)
    
    page = request.GET.get('page', 1)
    paginator = Paginator(following, 20)
    try:
        followings = paginator.page(page)
    except PageNotAnInteger:
        followings = paginator.page(1)
    except Emptyage:
        followings = paginator.page(paginator.num_pages)
    
    context = {"followings": followings}
    return render(request, "root/followers_page.html", context)
    

def report_comment(request):
    report_comment = Report.objects.all().values("id", "comment_id", "rule_broken", "report", "report_time", "reporter", "report_type")
    report_thread = ReportThread.objects.all().values("id", "thread_id", "rule_broken", "report", "report_time", "reporter", "report_type")
    reportUser = User.objects.all()
    reports = sorted(chain(report_comment, report_thread), key=itemgetter('report_time'), reverse=True)
    context = { "reports": reports, "reportUser": reportUser }
    seen_reports = Report.objects.filter(report_seen=True)
    seen_reports.delete()
    return render(request, "root/reports.html", context)
   
def followers_content(request):
    # get all data
    all_members = Category.objects.all()
    comment = Comment.objects.all()
    all_jobs = Job.objects.all() 
    all_polls = Poll.objects.all()
    all_blogs = Blog.objects.all()
    
    following = Following.objects.filter(follower_id=request.user.id)
    get_followers_list = chain(following.values("following"))
    hamlets = Members.objects.filter(user_id=request.user.id)
    serialized_ad = ads_manager("feeds", 3, request.user.id, request.user.profile.country)

    all_followers_thread = []
    for each_hamlet in hamlets:
        each_hamlet_threads = Thread.objects.filter(thread_category_id=each_hamlet.hamlet.id).values("datetime", "title", "details", "views", "image", "user_id", "id",)
        all_followers_thread.append(each_hamlet_threads)
    
    for each_follower in get_followers_list:
        shares = Share.objects.filter(sharer_id=each_follower['following']).values("content_id", "content_user_id", "content_type", "user_name", "datetime", "sharer_id")
        each_follower_threads = Thread.objects.filter(user_id=each_follower['following']).values("datetime", "title", "details", "views", "image", "user_id", "id",)
        comments = Comment.objects.filter(user_id=each_follower['following']).values("id", "comment", "thread_id", "datetime")
        polls = Poll.objects.filter(user_id=each_follower['following']).values("datetime", "title", "expiryDate", "slugTitle", "settled", "image", "user_id", "id",)
        jobs = Job.objects.filter(user_id=each_follower['following']).values("id", "address", "slugTitle", "name_of_company", "title", "category", "details", "jobImage", "datetime")
        blogs = Blog.objects.filter(user_id=each_follower['following']).values("datetime","tags", "slugTitle", "title", "category", "details", "image", "user_id", "id", "user")

        all_followers_thread.append(each_follower_threads)
        all_followers_thread.append(comments)
        all_followers_thread.append(polls)
        all_followers_thread.append(blogs)
        all_followers_thread.append(jobs)
        all_followers_thread.append(shares)

    get_followers_list = sorted(chain(*all_followers_thread), key=itemgetter('datetime'), reverse=True)
    
    followerslen = following.count()
    
    page = request.GET.get('page', 1)
    paginator = Paginator(get_followers_list, 15)
    try:
        following_paginator = paginator.page(page)
    except PageNotAnInteger:
        following_paginator = paginator.page(1)
    except EmptyPage:
        following_paginator = paginator.page(paginator.num_pages)

    context = { "followers": following_paginator, 'all_jobs': all_jobs, 'all_blogs': all_blogs, 'all_polls': all_polls, 'all_members': serializers.serialize('json', all_members), 'serialized_ad': serialized_ad, 'all_hamlets': all_members, "followerslen": followerslen, "comment": comment}
    return render(request, "root/followers_content.html", context)
    
def favourites(request):
    fav_thread = Favourite.objects.filter(user_id=request.user.id)
   
    page = request.GET.get('page', 1)
    paginator = Paginator(fav_thread, 20)
    try:
        favs = paginator.page(page)
    except PageNotAnInteger:
        favs = paginator.page(1)
    except EmptyPage:
        favs = paginator.page(paginator.num_pages)

    context = { "fav_thread": favs }
    return render(request, "root/favourite.html", context)

def signin(request): 
    if request.method == "POST":
        redirect_url = request.POST["redirect"]  
        if redirect_url == "":
            re = '/followers-content/'  
        else:
            re = redirect_url
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username.lower(), password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if redirect_url == "new":
                    re = f"/profile/update/{user.profile.id}/"

                return redirect(f'{re}') 
            else:
                messages.error(request, "Your account is disabled for now")
                return redirect('/login/')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login/')
          
def your_followers(request):
    following = Following.objects.filter(following_id=request.user.id)
    your_followings = Following.objects.filter(follower_id=request.user.id)    
    
    page = request.GET.get('page', 1)
    paginator = Paginator(following, 20)
    try:
        followings = paginator.page(page)
    except PageNotAnInteger:
        followings = paginator.page(1)
    except Emptyage:
        followings = paginator.page(paginator.num_pages)

    context = {"followings": followings, "your_followings": your_followings }
    return render(request, "root/your_followers.html", context)


def check_followers_profile(request, profile_id, profile_username):
    following = Following.objects.filter(follower_id=profile_id)
    your_followings = Following.objects.filter(follower_id=request.user.id)
   
    page = request.GET.get('page', 1)
    paginator = Paginator(following, 20)
    try:
        followings = paginator.page(page)
    except PageNotAnInteger:
        followings = paginator.page(1)
    except Emptyage:
        followings = paginator.page(paginator.num_pages)

    context = {"followings": followings, "your_followings": your_followings, "followers_name": profile_username }
    return render(request, "root/profile_follower.html", context)

def countrystats(request):
    all_countries = CountryStats.objects.all()
    context = { "all_countries": all_countries }
    return render(request, "root/countrystats.html", context)

