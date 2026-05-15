from django.contrib import admin
from .models import Profile

from .models import Category, Book, Comment, Evaluation, Favorite, Like, Notification, Resume
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Evaluation)
admin.site.register(Favorite)
admin.site.register(Like)

admin.site.register(Resume)
