from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField()
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="post_images", null=True, blank=True)


    def comments_count(self):
        return self.comments.count()


class Comment(models.Model):
    post = models.ForeignKey(to="Post", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
