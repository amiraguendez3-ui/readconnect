from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female')]
    )
    image = models.ImageField(upload_to='profiles/', default='default.png')

    def __str__(self):
        return self.user.username
# Categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


# Book
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    publication_date = models.DateField()
    image = models.ImageField(upload_to='books/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title


# Commentaire
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comments')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content[:20]


# Evaluation (Rating)
class Evaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='evaluations')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='evaluations')
    note = models.IntegerField()  # من 1 إلى 5

    def __str__(self):
        return f"{self.book.title} - {self.note}"

# Favori
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,related_name='favorite')
    added_date = models.DateField(auto_now_add=True)


# Like
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='likes')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='likes')


# Notification
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


# Resume
class Resume(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Resume of {self.book}"
