from django.urls import path
from . import views

urlpatterns = [
    # ── Home ──────────────────────────────────────────
    path('', views.home, name='home'),

    # ── Auth ──────────────────────────────────────────
    path('signup/',  views.signup,       name='signup'),
    path('login/',   views.login_views,  name='login'),

    # ── Categories ────────────────────────────────────
    path('categories/',                       views.categories_view, name='categories'),
    path('category/<str:name>/',              views.category_detail, name='category_detail'),
    path('category/<int:category_id>/books/', views.category_books,  name='category_books'),

    # ── Book ──────────────────────────────────────────
    path('book/<slug:slug>/',               views.book_detail,    name='book_detail'),
    path('rate-book/<int:book_id>/',        views.rate_book,      name='rate_book'),
    path('add-to-list/<int:book_id>/',      views.add_to_favorite, name='add_to_favorite'),
    path('add-comment/<int:book_id>/',      views.add_comment,    name='add_comment'),
    path('like-comment/<int:comment_id>/',  views.like_comment,   name='like_comment'),
    path('my-list/',                        views.my_list,        name='my_list'),

    # ── Discussion Groups ─────────────────────────────
    path('join-group/<int:book_id>/<str:group_type>/', views.join_group, name='join_group'),

    # ── Profile ───────────────────────────────────────
    path('profile/',                 views.profile_view,    name='profile'),
    path('profile/update/',          views.update_profile,  name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('delete-account/',          views.delete_account,  name='delete_account'),

    # ── Notifications ─────────────────────────────────
    path('notifications/',                           views.notifications_view,      name='notifications'),
    path('notifications/mark-read/<int:notif_id>/',  views.mark_notification_read,  name='mark_notif_read'),
    path('notifications/mark-all-read/',             views.mark_all_read,           name='mark_all_read'),
    path('notifications/clear-all/',                 views.clear_all_notifications, name='clear_all_notifs'),

    # ── Search ────────────────────────────────────────
    path('search-books/', views.search_books, name='search_books'),

    # ── Admin ─────────────────────────────────────────
    path('admin-dashboard/',                 views.admin_dashboard,    name='admin_dashboard'),
    path('admin/ban-user/<int:user_id>/',    views.ban_user,           name='ban_user'),
    path('admin/delete-user/<int:user_id>/', views.delete_user,        name='delete_user'),
    path('admin/delete-book/<int:book_id>/', views.admin_delete_book,  name='admin_delete_book'),
    path('admin/publish-book/',              views.publish_book,        name='publish_book'),



  path('group-chat/<int:book_id>/<str:group_type>/', views.group_chat,            name='group_chat'),
  path('group-chat/send/',                           views.send_group_message,     name='send_group_message'),
  path('group-chat/messages/',                       views.get_new_group_messages, name='get_new_group_messages'),
  path('logout/',                                    views.logout,                 name='logout'),
  path('my-groups/', views.my_groups, name='my_groups'),
  
]