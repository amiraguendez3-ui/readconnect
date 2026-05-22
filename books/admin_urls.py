# books/admin_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/book/delete/<int:book_id>/', views.admin_delete_book, name='admin_delete_book'),
    path('admin-dashboard/comment/delete/<int:comment_id>/', views.admin_delete_comment, name='admin_delete_comment'),
    path('admin-dashboard/user/delete/<int:user_id>/', views.delete_user, name='admin_delete_user'),
    path('admin-dashboard/user/ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('admin-dashboard/book/publish/', views.publish_book, name='publish_book'),
]