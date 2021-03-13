from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank= True, upload_to="images/")

    def __str__(self):
        return str(self.user)

class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete = models.CASCADE, verbose_name="Kullanıcı")
    title = models.CharField(max_length = 50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add = True, verbose_name="Oluşturma Tarihi")
    likes = models.ManyToManyField(User, related_name='blog_post')
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_date']

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete= models.CASCADE, verbose_name="Post", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.CharField(max_length=250, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_content

    class Meta:
        ordering = ['-comment_date']