from django.db import models
from django.contrib.auth.models import User 
from tinymce.models import HTMLField
# Create your models here.
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    details = HTMLField()#.TextField()
    datetime = models.DateTimeField()
    category = models.CharField(max_length=200)
    views = models.IntegerField(default=0)
    image = models.ImageField(upload_to="./blog_pic", blank=True)
    slugTitle = models.SlugField()
    tags = models.CharField(max_length=500)
    bloglike = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.category} \n {self.title}"
  
    def get_absolute_url(self):
        return f"/blog/each/?title={self.slugTitle}&value={self.id}"
    
class Blog_like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    blog_like = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    