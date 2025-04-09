from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

class Post(models.Model):
    content = models.TextField(blank = True, null = True)
    image = models.ImageField(upload_to = 'upload/posts/', validators = [FileExtensionValidator(['png', 'jpg', 'jpeg'])], blank = True, null = True)
    liked = models.ManyToManyField(User, blank = True, related_name = 'likes')
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'posts')

    def __str__(self):
        return str(self.content)

class Question(models.Model):
    post = models.ForeignKey(Post, related_name='questions', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='questions', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.body)


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'answer')

    def __str__(self):
        return f'{self.user.username} likes {self.answer.body}'