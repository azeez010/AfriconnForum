from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.utils import timezone
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

class Profile(models.Model):
    afrika_deeds = models.IntegerField(default=20)
    gender = models.CharField(max_length=100, default="none")
    about = models.TextField(blank=True)
    country = CountryField()
    city = models.CharField(max_length=50, default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    profile_pic = models.ImageField(upload_to="./profilePics", blank=True)
    job_tags = models.CharField(max_length=100, blank=True)
    are_you_currently_unemployed = models.BooleanField(default=False)
    last_seen = models.DateTimeField(default=timezone.now)
        
    def __str__(self):
        return f"{self.user.username} profile"   
    
    def get_absolute_url(self):
        return reverse("visit-profile", kwargs={"username": self.user.username})
    
        
class Following(models.Model):
    followBool = models.BooleanField(default=False)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")    
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ("-timestamp",)
         
class Sitesettings(models.Model):
    setting_name = models.CharField(max_length=100, default="")
    setting = models.CharField(max_length=100, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
# unimplemented models
class Transfer(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    fee = models.IntegerField(default=0)
    receiver_seen = models.BooleanField(default=True)
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cost = models.IntegerField()
    activity = models.CharField(max_length=200)
    

class Advert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expiryDate = models.IntegerField()
    cost = models.IntegerField()
    ad_country = models.CharField(max_length=5)
    advert_category = models.CharField(max_length=200)
    advert = models.ImageField(upload_to="./advert")
    advert_url = models.URLField()    
    advert_details = models.TextField(max_length=15000)
    approved = models.BooleanField(default=False) 
    ad_datetime = models.DateTimeField(default=timezone.now)
    ad_expirydatetime = models.DateTimeField(default=timezone.now)
    advert_title = models.CharField(max_length=800)
    advert_image_url = models.CharField(max_length=800, default="")
    
    def __str__(self):
        return f"{self.advert_url} by {self.user.username}"

class TransactionType(models.Model):
    cost = models.FloatField()
    activity = models.CharField(max_length=200)   

class Messages(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="send")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receive")
    msg = models.CharField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True)
    receiver_seen = models.BooleanField(default=True)
    msg_type = models.CharField(max_length=100)
    
    
class Ban(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    on_ban = models.BooleanField(default=False)
    expiry_time = models.IntegerField(blank=True)
    
    
    def __str__(self):
        return f"{user.username} banned for a day" 