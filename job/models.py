from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User 
from django.utils import timezone
from tinymce.models import HTMLField
# Create your models here.
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=450)
    details = HTMLField()
    address = models.CharField(max_length=4000)
    name_of_company = models.CharField(max_length=450)
    datetime = models.DateTimeField(default=timezone.now)
    slugTitle = models.CharField(max_length=450)
    fulfilled = models.BooleanField(default=False)
    pay = models.IntegerField(default=0)
    position = models.CharField(max_length=450)
    jobImage = models.ImageField(upload_to="job_images", default="./forum/static/portofolio.png", blank=True)
    category = models.CharField(max_length=450)
   
    def save(self, *args, **kwargs):
        if self.jobImage:
            # Opening the uploaded image
            im = Image.open(self.jobImage)
            output = BytesIO()
            # Resize/modify the image
            im = im.resize((200, 200))
            # after modifications, save it to the output
            im.save(output, format='JPEG', quality=90)
            output.seek(0)
            # change the imagefield value to be the newley modifed image value
            self.jobImage = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % self.jobImage.name.split('.')[0], 'image/jpeg',
                                            sys.getsizeof(output), None)
        super(Job, self).save(*args, **kwargs)
  
    
    def __str__(self):
        return f"{self.category} \n {self.title}"
    
    def get_absolute_url(self):
        return f"/jobs/jobpage/?title={self.slugTitle}&value={self.id}"
    
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applydate = models.DateTimeField()
    doc = models.FileField(upload_to="job_files", blank=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} applied"
    
class AlreadyApplied(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} already applied"
  