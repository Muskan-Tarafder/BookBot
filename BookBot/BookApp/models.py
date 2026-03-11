from django.db import models

# Create your models here.
# class Messages:

class Message(models.Model):
    role = models.CharField(max_length=10)
    content =  models.TextField()
    source = models.CharField(max_length=50,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=100,blank=True)

    def __str__(self):
        return f'[{self.role}] {self.content[:50]}'
    
    class Meta:
        ordering = ['timestamp']

class Suggestions(models.Model):
    suggestion = models.CharField(max_length=100)
    
    def __str__(self):
        return self.suggestion
    