from .models import Blog_like, Blog
from root.models import Profile
from django.shortcuts import render
import json

def likes(request):
    if request.is_ajax():
        if request.user.is_authenticated:
            user_id = request.user.id
        
        data = request.POST['data']
        order = json.loads(data)
        likes = order["blogBool"]
        blog_id = order["blog_id"]
        
        like = bool(likes)
        like_already_exists = Blog_like.objects.filter(user_id=user_id, blog_id=blog_id)
        blog = Blog.objects.filter(id=blog_id).first()
        if len(like_already_exists) == 0:
            blog.bloglike += 1
            blog.save()
            # update the user's point by increasing a point
            update_points = Profile.objects.get(user_id=blog.user.id)
            update_points.afrika_deeds += 1
            update_points.save()
            lk = Blog_like(user_id=user_id, blog_like=like,  blog_id=blog_id)
            lk.save()
        else:
            blog.bloglike -= 1
            blog.save()
            # update the user's point by decreasing a point
            update_points = Profile.objects.get(user_id=blog.user.id)
            update_points.afrika_deeds -= 1
            update_points.save()
            like_already_exists.delete()
                
    return render(request, "forum/home.html")
