from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):

    # Users post
    post_title = models.CharField(max_length=400)
    post_body = models.TextField(null=True,)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.post_title}'
    
class UserBio(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [('M','Male'), ('F', 'Female'), ('NB', 'Non Binary'), ('O', 'Other')]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='O')
    age = models.IntegerField()
    phone_num = models.IntegerField()
    country = models.CharField(max_length=50)
    about = models.CharField(max_length=400)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    comment = models.TextField()



# Create your models here.
