from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_views, name='login'),
    path('explore/', views.explore, name='explore'),
    path('categories/', views.categories_view, name='categories'),
    path('category/<str:name>/', views.category_detail, name='category_detail'),
    path('category/<int:category_id>/books/', views.category_books, name='category_books'),
    path('book/<slug:slug>/', views.book_detail, name='book_detail'),
    path('rate-book/<int:book_id>/', views.rate_book, name='rate_book'),
    path('add-to-list/<int:book_id>/', views.add_to_favorite, name='add_to_favorite'),
    path('add-comment/<int:book_id>/', views.add_comment, name='add_comment'),
    path('like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('my-list/', views.my_list, name='my_list'),
]