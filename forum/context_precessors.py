from .models import Thread, Comment, like_dislike, Reply, ThreadSeen, OnlineUser
from django.contrib.auth.models import User 
from root.models import Following, Sitesettings, Messages, Ban, Profile, Sitesettings 
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import itemgetter
from time import time
import datetime
from django.utils import timezone
import os
    

def home(request):
    new_replys = Reply.objects.filter(receiver_id=request.user.id, you_send=False, is_seen=False).count()
    new_comments = ThreadSeen.objects.filter(user_id=request.user.id, is_seen=False).count()

    expiredBans = Ban.objects.filter(expiry_time__lte = time())
    for expired in expiredBans:
        send_messages = Messages(sender_id=1, msg=f"<p class='tweet-color'>Your ban has been lifted</p>", receiver_id=expired.user_id, msg_type="ban expired", receiver_seen=False)
        send_messages.save() 
    
    expiredBans.delete()

    theme = Sitesettings.objects.filter(user_id=request.user.id, setting_name="theme").first()
    no_of_new_messages = Messages.objects.filter(receiver_id = request.user.id, receiver_seen=False).count()    

    user = User.objects.all()
    thread = Thread.objects.all()
    
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    expiry_time = time() + 1200
    objects, created = OnlineUser.objects.get_or_create(user_ip = ip, defaults={"last_seen": expiry_time,  "is_authenticated": request.user.is_authenticated})
    
    if request.user.is_authenticated:
        updateUserLastSeen = Profile.objects.get(user_id=request.user.id)
        updateUserLastSeen.last_seen = timezone.now()
        updateUserLastSeen.save()
        # deleting expired ip
        OnlineUser.objects.filter(last_seen__lte = time()).delete()
    
    if not created:
        objects.last_seen = time()
        objects.is_authenticated = request.user.is_authenticated
        objects.save()
    try:
        theme_color = Sitesettings.objects.get(setting_name = "theme_color", user_id=request.user.id)
        theme_color = theme_color.setting
    except Exception:
        theme_color = "orangered"
    #homepage
    return { "new_replies": new_replys, "new_messages": no_of_new_messages, "theme": theme, "new_comments": new_comments, "author": user, "thread": thread, "theme_color": theme_color}
