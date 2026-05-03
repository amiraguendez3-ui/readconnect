from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=[('male','Male'),('female','Female')], blank=True)
    image  = models.ImageField(upload_to='profiles/', default='default.png')

    def str(self):
        return self.user.username


class Category(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def str(self):
        return self.name


class Book(models.Model):
    title            = models.CharField(max_length=200)
    author           = models.CharField(max_length=100)
    description      = models.TextField(blank=True)
    publication_date = models.DateField(null=True, blank=True)
    image            = models.ImageField(upload_to='books/', null=True, blank=True)
    category         = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.title


class Comment(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.content[:20]


class Like(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    def str(self):
        return f"{self.user.username} liked comment {self.comment.id}"


class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='evaluations')
    note = models.IntegerField()

    def str(self):
        return f"{self.book.title} - {self.note}"


class Favorite(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='favorite')
    added_date = models.DateField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} - {self.book.title}"


class Notification(models.Model):
    TYPE_CHOICES = [
        ('like',     'Like'),
        ('comment',  'Comment'),
        ('reply',    'Reply'),
        ('new_book', 'New Book'),
        ('system',   'System'),
    ]
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    massage    = models.CharField(max_length=255)
    date       = models.DateTimeField(auto_now_add=True)
    is_read    = models.BooleanField(default=False)
    notif_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')

    def str(self):
        return f"{self.user.username} - {self.massage[:30]}"


class Resume(models.Model):
    book    = models.OneToOneField(Book, on_delete=models.CASCADE)
    content = models.TextField()

    def str(self):
        return f"Resume of {self.book}"
    
class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('reading', 'Currently Reading'),
        ('read',    'Already Read'),
    ]
    user      = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_statuses')
    book      = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_statuses')
    status    = models.CharField(max_length=10, choices=STATUS_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book') 

class GroupMessage(models.Model):
    book       = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='group_messages')
    user       = models.ForeignKey(User,   on_delete=models.CASCADE, related_name='group_messages')
    group_type = models.CharField(max_length=10)  # 'reading' or 'read'
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def str(self):
        return f"{self.user.username} in {self.group_type} — {self.book.title}"           