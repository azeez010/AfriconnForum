from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User 
from django.shortcuts import reverse
# Create your models here.
class Poll(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    expiryDate = models.IntegerField(default=0)
    image = models.ImageField(upload_to="poll_images", blank=True)
    slugTitle = models.SlugField()
    settled = models.BooleanField(default=False)
    datetime = models.DateTimeField(default=timezone.now)
    graph_made = models.BooleanField(default=False)
    graph = models.ImageField(upload_to="poll_graph_result", blank=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f"/polls/poll/?title={self.title}&value={self.id}"
    
class PollChoice(models.Model):
    votes = models.IntegerField(default=0)
    choice = models.CharField(max_length=420)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ["votes"]
    
    def __str__(self):
        return self.choice
    
class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.CharField(max_length=420)
    notify = models.BooleanField(default=False)
    
    