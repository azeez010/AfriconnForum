from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from tinymce.models import HTMLField 
from django.urls import reverse
from django_countries.fields import CountryField
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from time import time
import sys

      
class Category(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    created_at =  models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="./hamlet_pic", blank=True)
    name_of_creator = models.CharField(max_length=500)
    no_of_thread = models.IntegerField(default=0)
    no_of_member = models.IntegerField(default=0)
    image_url = models.CharField(default="", max_length=500)
    
    def save(self, *args, **kwargs):
        # Opening the uploaded image
        if self.image:
            im = Image.open(self.image)
            output = BytesIO()
            # Resize/modify the image
            im = im.resize((100, 100))
            # after modifications, save it to the output
            im.save(output, format='PNG', quality=90)
            output.seek(0)
            # change the imagefield value to be the newley modifed image value
            self.image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                            sys.getsizeof(output), None)
            
        super(Category, self).save(*args, **kwargs)
        # Save URL after saving image
        if self.image:
            super(Category, self).save(*args, **kwargs)
            
    def get_absolute_url(self):
        return reverse("category", kwargs={"pk": self.pk, "title": self.title})
    
    def __str__(self):
        return f"{self.title}"

    
class Share(models.Model):
    content_id = models.IntegerField()
    content_type = models.CharField(max_length=200) 
    content_user  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shared_content_user")
    user_name = models.CharField(max_length=100)
    sharer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="content_sharer_id")
    datetime = models.DateTimeField(default=timezone.now)
    
class CountryStats(models.Model):
    country = CountryField()
    no_of_user = models.IntegerField()


class Chat(models.Model):
    chat_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_sender")
    chat_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chat_receiver")
    
    def __str__(self):
        return f"{self.chat_sender.username} - {self.chat_receiver.username}"
    
class ChatMessage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    who_send = models.ForeignKey(User, on_delete=models.CASCADE, related_name="who_send")
    message = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)
    sort = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.who_send.username} - {self.message}"
    
    

class Members(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hamlet = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.hamlet.title}"
  

class OnlineUser(models.Model):
    user_ip = models.CharField(max_length=2000)
    last_seen = models.IntegerField(default=0)
    is_authenticated = models.BooleanField(default=False)
  
    def __str__(self):
        return f"{self.user_ip} - {self.last_seen}"

class Thread(models.Model):
    thread_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000)
    details = HTMLField()
    datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    recommendation = models.CharField(max_length=5000)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to="./thread_pic", blank=True)
    threadSlug = models.SlugField()
    last_comment_datetime = models.DateTimeField(default=timezone.now)
    last_comment_length = models.IntegerField(default=0)
    
    # content = HTMLField()
    def __str__(self):
        return f"{self.thread_category.title} \n {self.title}"

    
    def get_absolute_url(self):
        return f"/forum/thread/?hamlet={self.thread_category.title}&slug={self.threadSlug}&thread_no={self.id}"
    
class ThreadSeen(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.is_seen}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    comment = HTMLField()
    is_seen = models.BooleanField(default=False)
    datetime = models.DateTimeField()    
    image = models.ImageField(upload_to="./comment_pic")
    invite = models.IntegerField(default=0)    
    
    def __str__(self):
        return f"{self.comment}"

class like_dislike(models.Model):
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    each_dislike = models.BooleanField(default=False)
    each_like = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)     
  
class thread_like(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    each_dislike = models.BooleanField(default=False)
    each_like = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    views = models.IntegerField(default=0)  
    
class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)     
    fav_thread = models.URLField()
    title = models.CharField(max_length=5000)
    category = models.CharField(max_length=100)
    app = models.CharField(max_length=100)
    fav_id = models.IntegerField()
    datetime = models.DateTimeField(default=timezone.now)
    
class Reply(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver_id = models.IntegerField()
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    you_send = models.BooleanField(default=False) 
    comment = models.TextField()
    datetime = models.DateTimeField()    
    image = models.ImageField(upload_to="./comment_pic")
    timestamp = models.FloatField(default=time())
class Report(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    rule_broken = models.CharField(max_length=400)
    report = models.TextField()
    report_time = models.DateTimeField(default=timezone.now)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=30, default="comment")
    report_seen = models.CharField(max_length=30, default=False)

class ReportThread(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    rule_broken = models.CharField(max_length=400)
    report = models.TextField()
    report_time = models.DateTimeField(default=timezone.now)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=30, default="thread")
    report_seen = models.CharField(max_length=30, default=False)

class Homepage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)     
    expiryDate = models.IntegerField(default=0)
    
class waitingHomeThread(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)     
    time = models.IntegerField(default=0)
    
