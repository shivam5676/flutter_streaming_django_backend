from django.db import models
class videoFiles(models.Model):
    path=models.FileField(upload_to="videos/")
    userId=models.IntegerField()
    createdAt=models.DateField()
    def __str__(self):
        return f"VideoFile(userId={self.userId}, createdAt={self.cretaedAt})"
    
# Create your models here.

class adsVideos(models.Model):
  
  path=models.FileField(upload_to="adsVideos/")
  userId=models.IntegerField()
  createdAt=models.DateField()
  def __str__(self):
        return self.path