from django.db import models
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)

class News_paper(models.Model):
    paper_id = models.AutoField(primary_key=True)
    
    categary = models.CharField(max_length=255)
    source=models.CharField(max_length=255)
    location=models.CharField(max_length=255)
    date=models.DateTimeField(null=True, blank=True)
    news_description=models.TextField()

class Comments(models.Model):
    comment_id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    paper_id=models.ForeignKey(News_paper,on_delete=models.CASCADE)
    comment_text=models.TextField()