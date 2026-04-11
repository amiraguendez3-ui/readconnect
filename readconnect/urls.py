"""
URL configuration for readconnect project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books.views import home
from books import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),  # هذا أهم سطر
    path('',include('books.urls')),

    path('signup/', views.signup, name='signup'),
     path('login/', views.login_views, name='login'),
     path('categories/', views.categories_view, name='categories'),
     path('category/', views.category_detail, name='category_detail'),
    path('explore/', views.explore, name='explore'),
    path('my-list/',views.my_list,name='my_list'),
         
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)