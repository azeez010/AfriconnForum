from .models import Following, Transfer, Profile, Sitesettings, Advert, Messages
from forum.models import Homepage, waitingHomeThread
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from time import time
from datetime import datetime

def follow(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        follows = order["blogBool"]
        follow_id = order["follow_id"]
        
        follow = bool(follows)
        follow_already_exists = Following.objects.filter(following_id=follow_id, follower_id=request.user.id)

        if len(follow_already_exists) == 0:
            lk = Following(following_id=follow_id, follower_id=request.user.id, followBool=follow)
            send_messages = Messages(sender_id=request.user.id, msg=f"{request.user.username} started following you", receiver_id=follow_id, msg_type="following", receiver_seen=False)
            send_messages.save()

            lk.save()
        else:
            send_messages = Messages(sender_id=request.user.id, msg=f"{request.user.username} unfollowed you", receiver_id=follow_id, msg_type="following", receiver_seen=False)
            send_messages.save()
            follow_already_exists.delete()
                
    return render(request, "forum/home.html")

        
def theme(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
            data = request.POST['data']
            theme = json.loads(data)
            # taking likes and dislikes
            site_theme = theme["theme"]
            
            set_name = theme["name"]
            
            settings_already_exists = Sitesettings.objects.filter(user_id=user_id, setting_name=set_name)

            if len(settings_already_exists) == 0:
                setting = Sitesettings(user_id=user_id, setting_name=set_name, setting=site_theme)
                setting.save()
                
            else:
                update = settings_already_exists.first()
                update.setting = site_theme
                update.save()
                
        return render(request, "forum/home.html")
        
def approved(request):
    ad_id = request.GET['id']
    # try:
    ad_update = Advert.objects.get(id=ad_id) 
    ad_duration = ad_update.expiryDate + time()
    expiryDate = datetime.fromtimestamp(ad_duration)
    
    # update the ads
    ad_update.approved = True 
    ad_update.expiryDate = ad_duration
    ad_update.ad_expirydatetime = expiryDate
    ad_update.save()       

    send_messages = Messages(sender_id=request.user.id, msg=f"<p class='whatsapp-this'>Your ads has being approved, and it will expire on {expiryDate}</p>", receiver_id=ad_update.user_id, msg_type="ads success", receiver_seen=False)
    send_messages.save()

    messages.success(request, f"{request.user.username}, you have successfully approved this post")
    return redirect("/ads-approval/")

def reject(request):
    cost = request.GET["cost"]
    ad_id = request.GET['id']
    try:
        advert = Advert.objects.get(id=ad_id)
        # send message
        send_messages = Messages(sender_id=request.user.id, msg=f"<p style='color: red'>Your ads has being rejected due to breaking of our policy, and your points refunded read our user policy and apply again </p>", receiver_id=advert.user_id, msg_type="ads failed", receiver_seen=False)
        send_messages.save()
        # refund points
        update_points = Profile.objects.get(user_id=advert.user_id)
        update_points.afrika_deeds += int(cost)
        update_points.save()
        advert.delete()
        
        messages.error(request, f"{request.user.username}, you have successfully rejected this post")
        return redirect("/ads-approval/")
    except:
        messages.error(request, f"{request.user.username}, sorry that ad does not exist")
        return redirect("/ads-approval/")

def message_admin(request):
    message = request.POST["message"]
    if message:
        send_messages = Messages(sender_id=request.user.id, msg=message, receiver_id=1, msg_type="admin message", receiver_seen=False)
        send_messages.save()
        messages.success(request, f"{request.user.username}, You have successfully sent the admin a message, you complain will be attended to as soon as possible")
        return redirect("/profile/")
    else:
        messages.error(request, f"{request.user.username}, enter something into the message box ")
        return redirect("/profile/")

        
def remove_homethread(request):
    homepageThreads = Homepage.objects.all()
    context = { "homepageThreads": homepageThreads}
    return render(request, "root/remove_homethread.html", context)
    
        
def remove_home(request):
    home_id = request.GET["id"]
    message = "Your thread has been removed from home thread because it violates our term of use <a class='tweet-this' href='/info/#terms'>term of use</a>" 
    send_messages = Messages(sender_id=request.user.id, msg=message, receiver_id=1, msg_type="admin message", receiver_seen=False)
    send_messages.save()
    
    #delete the home thread
    homepageThreads = Homepage.objects.filter(id=home_id)
    waitingthread = waitingHomeThread.objects.all()[:1]
    for each_waiting_thread in waitingthread:
        homethread = Homepage(user_id=each_waiting_thread.user_id, thread_id=each_waiting_thread.thread_id, expiryDate=each_waiting_thread.time + int(time()))
        homethread.save()
        each_waiting_thread.delete()
            
    
    homepageThreads.delete()
    messages.success(request, f"{request.user.username}, you have successfully remove this home thread")
    return redirect("/remove-homethread/")
    