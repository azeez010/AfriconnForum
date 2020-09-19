from django.contrib import admin
from .models import Thread, Comment, like_dislike, thread_like, Reply, Favourite, ThreadSeen, OnlineUser
# Register your models here.
admin.site.register(Thread)
admin.site.register(Comment)
admin.site.register(like_dislike)
admin.site.register(Favourite)
admin.site.register(thread_like)
admin.site.register(Reply)
admin.site.register(ThreadSeen)
admin.site.register(OnlineUser)