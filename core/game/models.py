from django.db import models

# Create your models here.

class Chapter(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Game(models.Model):
    title = models.CharField(max_length=255)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    xp = models.IntegerField(default=2000)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
