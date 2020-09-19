from django.shortcuts import render, redirect
from .forms import Register_user, create_comment, create_thread
from .models import Category, like_dislike, Comment, thread_like, Favourite, Reply, ThreadSeen, Share, Members, Category, Chat, ChatMessage
from root.models import Profile, Messages, Sitesettings
from django.contrib.auth.models import User 
import json
from datetime import datetime
from django.http import JsonResponse
from itertools import chain
from operator import itemgetter
from django.core import serializers
from time import time    

def likes(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        # taking likes and dislikes
        dislikes = order["dislike"]
        likes = order["like"]
        comment_id = order["comment_id"]
        author_id = order["author"]
        button = order["button"]
      
        dislikes = True if dislikes == 1 else False
        likes = True if likes == 1 else False 

        like_already_exists = like_dislike.objects.filter(user_id=user_id, comments_id=comment_id)

        if len(like_already_exists) == 0:
            lk = like_dislike(user_id=user_id, comments_id=comment_id, each_like=likes, each_dislike=dislikes)
            if dislikes:
                # decrease points
                points = Profile.objects.get(user_id=author_id)
                points.afrika_deeds -= 1
                points.save() 

            if likes:
                # increase points
                points = Profile.objects.get(user_id=author_id)
                points.afrika_deeds += 1
                points.save()
            
            lk.save()    
        else:
            if dislikes == False and likes == False:
                update = like_already_exists.first()
                points = Profile.objects.get(user_id=author_id)
                if button == "like" and update.each_like == True:
                    points.afrika_deeds -= 1
                if button == "hate" and update.each_dislike == True:
                    points.afrika_deeds += 1
                
                like_already_exists.delete()
                points.save()
            else:
                update = like_already_exists.first()
                
                if dislikes and update.each_dislike == False:
                    # decrease points
                    points = Profile.objects.get(user_id=author_id)
                    points.afrika_deeds -= 1
                    points.save() 
                    update.each_like = likes
                    update.each_dislike = dislikes
                    update.save()

                if likes and update.each_like == False:
                    # increase points
                    points = Profile.objects.get(user_id=author_id)
                    points.afrika_deeds += 1
                    points.save()
                    update.each_like = likes
                    update.each_dislike = dislikes
                    update.save()
                
    return render(request, "forum/home.html")

def threadLikes(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        # taking likes and dislikes
        dislikes = order["dislike"]
        likes = order["like"]
        thread_id = order["thread_id"]
        # to know which button is clicked upon
        button = order["button"]

        dislikes = True if dislikes == 1 else False
        likes = True if likes == 1 else False
      

        threadLike_already_exists = thread_like.objects.filter(user_id=user_id, thread_id=thread_id)

        if len(threadLike_already_exists) == 0:
            thread_lk = thread_like(user_id=user_id, thread_id=thread_id, each_like=likes, each_dislike=dislikes)
            if dislikes:
                # decrease points
                points = Profile.objects.get(user_id=user_id)
                points.afrika_deeds -= 1
                points.save() 

        
            if likes:
                # increase points
                points = Profile.objects.get(user_id=user_id)
                points.afrika_deeds += 1
                points.save()

            thread_lk.save()
            
        else:
            if dislikes == False and likes == False:
                update = threadLike_already_exists.first()
                points = Profile.objects.get(user_id=user_id)
                if button == "like"  and update.each_like == True:
                    points.afrika_deeds -= 1
                if button == "hate"  and update.each_dislike == True:
                    points.afrika_deeds += 1
                
                threadLike_already_exists.delete()
                points.save()

            else:
                update = threadLike_already_exists.first()
               
                if dislikes and update.each_dislike == False:
                    # decrease points
                    points = Profile.objects.get(user_id=user_id)
                    points.afrika_deeds -= 1
                    points.save() 
                    update.each_like = likes
                    update.each_dislike = dislikes
                    update.save()
             

                if likes and update.each_like == False:
                    # increase points
                    points = Profile.objects.get(user_id=user_id)
                    points.afrika_deeds += 1
                    points.save()
                    update.each_like = likes
                    update.each_dislike = dislikes
                    update.save()
                    
             
    return render(request, "forum/home.html")
    
def favourite(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        # taking likes and dislikes
        href = order["href"]
        fav_id = order["thread_id"]
        category = order["category"]
        title = order["title"]
        app = order["app"]
        toggleBool = bool(order["toggleBool"])

        if toggleBool:
            fav = Favourite(user_id=user_id, app=app, fav_id=fav_id, title=title, category=category, fav_thread=href)
            fav.save()
            
        else:
            favourite_already_exists = Favourite.objects.filter(user_id=user_id, fav_id=fav_id, title=title)
            favourite_already_exists.delete()
                
    return render(request, "forum/home.html")

def reply(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        
        sender_id = order["sender_id"]
        comment_id = order["comment_id"]
        receiver_id = order["receiver_id"]
        reply_message = order["replyMessage"]
        you_send = True if receiver_id == sender_id else False
        
        reply = Reply(receiver_id=receiver_id, you_send=you_send, sender_id=sender_id, comments_id=comment_id, comment=reply_message, datetime=datetime.now())
        reply.save()
        # message_all_replyers = 
                    
    return render(request, "forum/home.html")

def seen(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        
        isSeen = bool(order["is_seen"])
        comment_id = order["comment_id"]
        reply = Reply.objects.get(is_seen=False, receiver_id=user_id, comments_id=comment_id)
        reply.is_seen = isSeen
        reply.save()
                    
    return render(request, "forum/home.html")

def getReply(request, comment_id):
    if request.is_ajax():
        # try:
        reply = Reply.objects.filter(comments_id=comment_id)
        replyData = []
        for each_reply in reply:
            sender_id = User.objects.get(id=each_reply.sender_id)
            Date = each_reply.datetime.strftime("%d %b %Y %I-%M%p")
            if Date[0] == "0":
                Date = Date[1:]
            replyData.append({"comment": each_reply.comment, "datetime": Date, "image": "", "sender_name": sender_id.username, "sender_id": each_reply.sender_id, "comment_id": each_reply.comments_id, "receiver_id": each_reply.receiver_id, "timestamp": each_reply.timestamp })
        
        return JsonResponse({"data": replyData})
    
def seenThread(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        
        isSeen = bool(order["is_seen"])
        thread_id = order["thread_id"]
        seeThread = ThreadSeen.objects.get(is_seen=False, user_id=user_id, thread_id=thread_id)
        seeThread.is_seen = isSeen
        seeThread.save()
                    
    return render(request, "forum/home.html")

def updateThreadSeen(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        ThreadSeenData = json.loads(data)
        thread_id = ThreadSeenData["thread_seen_id"]
        
        try:
            deleteThreadComment = ThreadSeen.objects.get(thread_id=thread_id, user_id=request.user.id) 
            deleteThreadComment.delete()
        except error:
            print(error)

        return render(request, "forum/home.html")

def remove_message(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        messageData = json.loads(data)
        msg_type = messageData["msg_type"]
        receiver_id = messageData["receiver_id"]
        sender_id = messageData["sender_id"]
        msg = messageData["msg"]
        # time = messageData["time"]
        message_id = messageData["message_id"]
        
        deleteMessage = Messages.objects.get(msg=msg, id=message_id,  sender_id=sender_id, receiver_id=receiver_id, msg_type=msg_type) 
        deleteMessage.delete()
        # except error:
        #     print("error")

        return render(request, "forum/home.html")
    
def join_hamlet(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
            
            data = request.POST['data']
            messageData = json.loads(data)
            user_id = messageData["user_id"]
            hamlet_id = messageData["hamlet_id"]
            description = messageData["description"]
            is_a_member = bool(messageData["is_a_member"])
            if is_a_member:
                Members.objects.get_or_create(user_id=user_id, hamlet_id=hamlet_id, description=description)
                all_hamlet_members = Members.objects.filter(hamlet_id=hamlet_id )
                update_hamlet_member_no = Category.objects.get(id=hamlet_id)
                update_hamlet_member_no.no_of_member = all_hamlet_members.count()
                update_hamlet_member_no.save()
            else:
                remove_member_from_group = Members.objects.filter(user_id=user_id, hamlet_id=hamlet_id )
                remove_member_from_group.delete()
                all_hamlet_members = Members.objects.filter(hamlet_id=hamlet_id )
                update_hamlet_member_no = Category.objects.get(id=hamlet_id )
                update_hamlet_member_no.no_of_member = all_hamlet_members.count()
                update_hamlet_member_no.save()
            return render(request, "forum/home.html")

def send_chat(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        messageData = json.loads(data)
        message = messageData["message"]
        receiver_id = messageData["receiver_id"]
        sender_id = messageData["sender_id"]
        sender_name = messageData["sender_name"]
        chatgroup, created =  Chat.objects.get_or_create(chat_sender_id=sender_id, chat_receiver_id=receiver_id)
        create_chat = ChatMessage.objects.create(chat_id=chatgroup.id, message=message, who_send_id=sender_id, sort=time())
        create_chat.save()
        msg = f"<a href='/forum/chat/{sender_id}/'>you have a new message from {sender_name}<br><span class='tweet-color'>{message}<span></a>"
        Messages.objects.create(msg=msg,  receiver_seen=False, sender_id=sender_id, receiver_id=receiver_id, msg_type="chat")
        return render(request, "forum/home.html")    
        
def update_chat(request, chat_id, previous_list_no):
    if request.is_ajax():
        # try:
        chats = []
    
        your_chats = Chat.objects.filter(chat_sender=request.user.id, chat_receiver=chat_id)
        if your_chats.exists():
            messages = ChatMessage.objects.filter(chat_id=your_chats.first().id).values("datetime", "who_send", "message" )
            chats.append(messages)
            
        
        other_person_chat  = Chat.objects.filter(chat_sender=chat_id, chat_receiver=request.user.id)
        if other_person_chat .exists():
            messages = ChatMessage.objects.filter(chat_id=other_person_chat .first().id).values("datetime", "who_send", "message" )
            chats.append(messages)
        
        other_person_details = User.objects.get(id=chat_id)
        
        chat_list = sorted(chain(*chats), key=itemgetter('datetime'))
        
        update_list = chat_list[int(previous_list_no):]
        
        return JsonResponse({"data": update_list})
      
def filcat(request, text):
    if request.is_ajax():
        pattern = text.replace(" ", "|")
        search = pattern
        if pattern != "":
            search = r"({})".format(pattern)
        print(search)
        hamlets = Category.objects.filter(title__iregex=r'{}'.format(search))
        hamletsData = serializers.serialize('json', hamlets)
        return JsonResponse(hamletsData, safe=False)

def share(request):
    if request.is_ajax() and request.user.is_authenticated:
        data = request.POST['data']
        shareData = json.loads(data)
        app = shareData["app"]
        share_id = shareData["share_id"]
        content_owner = shareData["content_owner"]
        Share.objects.create(content_type=app, content_id=share_id, content_user_id=content_owner, user_name=request.user.username, sharer_id=request.user.id)
        
        
    return render(request, "forum/home.html")    
        
def theme_color(request):
    data = request.POST['data']
    colorValue = json.loads(data)
    color = colorValue["color"]
    Sitesettings.objects.update_or_create(setting_name = "theme_color", user_id=request.user.id, defaults={"setting": color})
    return render(request, "forum/home.html") 

def edit_reply(request):
    data = request.POST['data']
    replyData = json.loads(data)
    comments_id = replyData['comment_id']
    sender_id = replyData['sender_id']
    receiver_id = replyData['receiver_id']
    newComment = replyData['newComment']
    timestamp = replyData['timestamp']
    editReply = Reply.objects.get(timestamp=timestamp, comments_id=comments_id, sender_id=sender_id, receiver_id=receiver_id)
    editReply.comment = newComment
    editReply.save()
    return render(request, "forum/home.html") 