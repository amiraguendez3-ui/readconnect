from django.shortcuts import render, get_object_or_404, redirect 
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse 
from django.contrib.auth.decorators import login_required 
from django.db.models import Avg, Count 
from django.contrib.auth import update_session_auth_hash 
from django.contrib import messages 
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.admin.views.decorators import staff_member_required 
from django.contrib.auth.models import User 
from django.utils import timezone 
from django.db.models.functions import Coalesce 
from django.db.models import Value, FloatField, F 
from datetime import timedelta 
from django.views.decorators.http import require_POST
import json 
from .models import Category, Book 
from django.http import JsonResponse 
from django.template.defaultfilters import slugify 
from django.db import models 
 
from .models import Book, Category, Comment, Evaluation, Favorite, Like, Notification, ReadingStatus 
from django.contrib.auth import authenticate, login as auth_login, logout 
from django.contrib.auth.models import User 
from django.shortcuts import render, redirect 
from .models import Profile 
from .models import GroupMessage 

 # ================================================================
# التعديلات المطلوبة في views.py
# أضف هذه الدالة المساعدة + عدّل دالة home()
# ================================================================

# -------- 1) أضف هذه الدالة المساعدة في أعلى views.py (بعد الـ imports) --------

def get_category_svg(name):
    """
    ترجع SVG مناسب لكل category حسب اسمها.
    النمط: خط نظيف (outline) مثل الصورة المرجعية.
    """
    name_lower = name.lower().strip()

    svgs = {
        # ===== Fiction / روايات =====
        'fiction': '<svg viewBox="0 0 24 24" fill="none" stroke="#ae6a97" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
        'رواية': '<svg viewBox="0 0 24 24" fill="none" stroke="#ae6a97" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
        'روايات': '<svg viewBox="0 0 24 24" fill="none" stroke="#ae6a97" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',

        # ===== Romance / رومانس =====
        'romance': '<svg viewBox="0 0 24 24" fill="none" stroke="#e05080" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/></svg>',
        'رومانس': '<svg viewBox="0 0 24 24" fill="none" stroke="#e05080" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/></svg>',
        'رومانسية': '<svg viewBox="0 0 24 24" fill="none" stroke="#e05080" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/></svg>',

        # ===== Mystery / غموض =====
        'mystery': '<svg viewBox="0 0 24 24" fill="none" stroke="#ae6a97" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',

        # ===== Thriller / إثارة =====
        'thriller': '<svg viewBox="0 0 24 24" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
        'جريمة': '<svg viewBox="0 0 24 24" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',

        # ===== Fantasy =====
        'fantasy': '<svg viewBox="0 0 24 24" fill="none" stroke="#7b5ea7" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',

        # ===== Science Fiction =====
        'science fiction (sci-fi)': '<svg viewBox="0 0 24 24" fill="none" stroke="#2980b9" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
        'sci-fi': '<svg viewBox="0 0 24 24" fill="none" stroke="#2980b9" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
        'خيال علمي': '<svg viewBox="0 0 24 24" fill="none" stroke="#2980b9" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',

        # ===== Horror / رعب =====
        'horror': '<svg viewBox="0 0 24 24" fill="none" stroke="#6c3483" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 15s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',
        'رعب': '<svg viewBox="0 0 24 24" fill="none" stroke="#6c3483" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 15s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',

        # ===== History / تاريخ =====
        'history': '<svg viewBox="0 0 24 24" fill="none" stroke="#8e6b3e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        'historical fiction': '<svg viewBox="0 0 24 24" fill="none" stroke="#8e6b3e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        'تاريخ': '<svg viewBox="0 0 24 24" fill="none" stroke="#8e6b3e" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',

        # ===== Adventure / مغامرة =====
        'adventure': '<svg viewBox="0 0 24 24" fill="none" stroke="#27ae60" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>',
        'مغامرة': '<svg viewBox="0 0 24 24" fill="none" stroke="#27ae60" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="3 11 22 2 13 21 11 13 3 11"/></svg>',

        # ===== Self-development =====
        'self-development (self-help)': '<svg viewBox="0 0 24 24" fill="none" stroke="#f39c12" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        'self-help': '<svg viewBox="0 0 24 24" fill="none" stroke="#f39c12" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        'تطوير الذات': '<svg viewBox="0 0 24 24" fill="none" stroke="#f39c12" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',

        # ===== Biography / سيرة ذاتية =====
        'biography': '<svg viewBox="0 0 24 24" fill="none" stroke="#561d46" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        'autobiography': '<svg viewBox="0 0 24 24" fill="none" stroke="#561d46" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
        'سيرة ذاتية': '<svg viewBox="0 0 24 24" fill="none" stroke="#561d46" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>',
       # ===== Drama =====
        'drama': '<svg viewBox="0 0 24 24" fill="none" stroke="#8e44ad" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>',

        # ===== Young Adult =====
        'young adult (ya)': '<svg viewBox="0 0 24 24" fill="none" stroke="#e67e22" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>',

        # ===== Children Literature =====
        "children's literature": '<svg viewBox="0 0 24 24" fill="none" stroke="#1abc9c" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        'childrens literature': '<svg viewBox="0 0 24 24" fill="none" stroke="#1abc9c" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
        'أطفال': '<svg viewBox="0 0 24 24" fill="none" stroke="#1abc9c" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',

        # ===== Poetry / شعر =====
        'poetry': '<svg viewBox="0 0 24 24" fill="none" stroke="#9b59b6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',
        'شعر': '<svg viewBox="0 0 24 24" fill="none" stroke="#9b59b6" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>',

        # ===== Graphic Novel =====
        'graphic novel / comics': '<svg viewBox="0 0 24 24" fill="none" stroke="#e74c3c" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',

        # ===== Dystopian / Utopian =====
        'dystopian': '<svg viewBox="0 0 24 24" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
        'utopian': '<svg viewBox="0 0 24 24" fill="none" stroke="#27ae60" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',

        # ===== Satire =====
        'satire': '<svg viewBox="0 0 24 24" fill="none" stroke="#f39c12" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 13s1.5 3 4 3 4-3 4-3"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>',

        # ===== Crime / Paranormal =====
        'crime': '<svg viewBox="0 0 24 24" fill="none" stroke="#c0392b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
        'paranormal': '<svg viewBox="0 0 24 24" fill="none" stroke="#6c3483" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg>',

        # ===== Memoir / Travel =====
        'memoir': '<svg viewBox="0 0 24 24" fill="none" stroke="#2c3e50" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/></svg>',
        'travel': '<svg viewBox="0 0 24 24" fill="none" stroke="#16a085" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
        'سفر': '<svg viewBox="0 0 24 24" fill="none" stroke="#16a085" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',

        # ===== Health / صحة =====
        'health': '<svg viewBox="0 0 24 24" fill="none" stroke="#27ae60" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',
        'صحة': '<svg viewBox="0 0 24 24" fill="none" stroke="#27ae60" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>',

        # ===== Default =====
        'default': '<svg viewBox="0 0 24 24" fill="none" stroke="#ae6a97" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    }

    return svgs.get(name_lower, svgs['default'])


# -------- 2) عدّل دالة home() بإضافة featured_categories --------

COLOR_CLASSES = ['purple', 'yellow', 'pink', 'blue', 'beige', 'green', 'orange', 'cyan']
def home(request):
    new_books = Book.objects.order_by('-created_at')[:8]
    best_books = Book.objects.annotate(
        avg_note=Coalesce(Avg('evaluations__note'), Value(0.0), output_field=FloatField())
    ).order_by('-avg_note')[:8]
    trending_books = Book.objects.annotate(
        total_favorites=Count('favorite'),
        total_likes=Count('comments__likes'),
        total_comments=Count('comments'),
        total_evaluations=Count('evaluations'),
        trending_score=F('total_likes')*2 + F('total_comments')*3 + F('total_evaluations')*1 + F('total_favorites')*2
    ).order_by('-trending_score')[:8]
    top_users = User.objects.annotate(
        total_interactions=Count('comments') + Count('likes') + Count('evaluations') + Count('favorites')
    ).order_by('-total_interactions')[:8]

    # ---- الجديد: featured_categories من قاعدة البيانات مع SVG icon ----
    all_categories = Category.objects.all()
    featured_categories = []
    for i, cat in enumerate(all_categories[:6]):   # أول 6 categories في الـ home
        featured_categories.append({
            'id': cat.id,
            'name': cat.name,
            'color_class': COLOR_CLASSES[i % 8],
            'svg_icon': get_category_svg(cat.name),
        })

    return render(request, 'home.html', {
        'new_books': new_books,
        'best_books': best_books,
        'trending_books': trending_books,
        'top_users': top_users,
        'featured_categories': featured_categories,   # <-- جديد
    })
 
 
# ========== تسجيل / دخول ========== 
 
 
def login_views(request): 
    if request.user.is_authenticated: 
        return redirect('/') 
     
    error = None 
    if request.method == 'POST': 
        username = request.POST.get('username') 
        password = request.POST.get('password') 
         
        user = authenticate(request, username=username, password=password) 
        if user is not None: 
            auth_login(request, user) 
            return redirect('/') 
        else: 
            error = 'Invalid username or password. Please try again.' 
     
    return render(request, 'login.html', {'error': error}) 
 
def signup(request): 
    if request.user.is_authenticated: 
        return redirect('/') 
     
    error = None 
    success = None 
     
    if request.method == 'POST': 
        first_name = request.POST.get('first_name') 
        last_name = request.POST.get('last_name') 
        email = request.POST.get('email') 
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        confirm_password = request.POST.get('confirm_password') 
        gender = request.POST.get('gender') 
         
        # Validation 
        if password != confirm_password: 
            error = 'Passwords do not match.' 
        elif User.objects.filter(username=username).exists(): 
            error = 'Username already exists. Please choose another.' 
        elif User.objects.filter(email=email).exists(): 
            error = 'Email already registered.' 
        elif len(password) < 6: 
            error = 'Password must be at least 6 characters.'
        else: 
            # Create user 
            user = User.objects.create_user( 
                username=username, 
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name 
            ) 
             
            # Create profile 
            Profile.objects.create(user=user, gender=gender) 
             
            # Auto login 
            auth_login(request, user) 
            return redirect('/') 
     
    return render(request, 'signup.html', {'error': error, 'success': success}) 
 
# ========== التصنيفات ========== 
def categories_view(request): 
    
    categories = Category.objects.all() 
 
    categories_with_books = [] 
    total_books = Book.objects.count() 
     
    for cat in categories: 
        books = cat.book_set.all()[:6]  # أول 6 كتب 
        categories_with_books.append({ 
            'id': cat.id, 
            'name': cat.name, 
            'title': cat.name.capitalize(), 
            'icon': '📚',  # أو يمكن جلب أيقونة من قاعدة البيانات إن وُجدت 
            'books': books, 
            'book_count': cat.book_set.count(),  # سنخفي هذا الرقم في القالب 
        }) 
     
     
 
    # الأيقونات تعتمد على اسم التصنيف الموجود في قاعدة البيانات 
    icons_map = { 
        # عربي 
        'روايات': '📖', 'رواية': '📖', 
        'علوم': '🧪', 'علم': '🧪', 
        'تاريخ': '🏛️', 
        'تطوير الذات': '💡', 'تطوير': '💡', 
        'أعمال': '📊', 'اعمال': '📊', 
        'دين': '☪️', 'اسلام': '☪️', 
        'فلسفة': '🤔', 
        'شعر': '✒️', 
        'أطفال': '🧸', 'اطفال': '🧸', 
        'طبخ': '🍔', 
        'صحة': '🩺', 
        'رياضة': '⚽️', 
        'سفر': '🗺️', 
        'سياسة': '🏛️', 
        'اقتصاد': '💰', 
        'تكنولوجيا': '💻', 
        'فن': '🎨', 
        'موسيقى': '🎵', 
        'سيرة ذاتية': '📝', 
        'خيال علمي': '🚀', 
        'رعب': '👻', 
        'جريمة': '🔪', 
        'مغامرة': '🧭', 
        'رومانسية': '💖', 'رومانس': '💖', 
        # إنجليزي 
        'fiction': '📖', 
        'science': '🧪', 
        'history': '🏛️', 
        'selfhelp': '💡', 'self-help': '💡', 'self help': '💡', 
        'business': '📊', 
        'religion': '☪️', 
        'philosophy': '🤔', 
        'poetry': '✒️', 
        'children': '🧸', 
        'food': '🍔', 
        'health': '🩺', 
        'sports': '⚽️', 
        'travel': '🗺️', 
        'politics': '🏛️', 
        'economics': '💰', 
        'technology': '💻', 
        'arts': '🎨', 
        'music': '🎵', 
        'biography': '📝', 
        'scifi': '🚀', 'sci-fi': '🚀', 
        'horror': '👻', 
        'thriller': '🔪', 
        'adventure': '🧭', 
        'romance': '💖', 
    } 
     
 
    categories_with_books = [] 
    total_books = 0 
 
    for category in categories: 
        books = category.book_set.all()[:6] 
        book_count = category.book_set.count() 
        total_books += book_count 
        name_lower = category.name.lower().strip() 
        categories_with_books.append({ 
            'id': category.id, 
            'name': category.name, 
            'title': category.name.capitalize(), 
            'icon': icons_map.get(name_lower, '📚'), 
            'books': books, 
            'book_count': book_count, 
        }) 
    return render(request, 'categories.html', { 
        'categories_with_books': categories_with_books, 
        'total_books': total_books, 
        'user': request.user,  # لاسم المستخدم 
    }) 
 
 
 
def category_books(request, category_id): 
    category = get_object_or_404(Category, id=category_id) 
    books = Book.objects.filter(category=category) 
    categories = Category.objects.all() 
    return render(request, 'category_books.html', { 
        'category': category, 
        'books': books, 
        'categories': categories,
}) 
 
def category_detail(request, name): 
    return render(request, "category_detail.html", {"name": name}) 
 
 
# ========== تفاصيل الكتاب ========== 
def book_detail(request, slug): 
    book = get_object_or_404(Book, title__iexact=slug.replace('-', ' ')) 
    avg_rating = Evaluation.objects.filter(book=book).aggregate(avg=Avg('note'))['avg'] or 0 
    ratings_count = Evaluation.objects.filter(book=book).count() 
    comments = book.comments.all().annotate(likes_count=Count('likes')).order_by('-created_at') 
    tags = [book.category.name] if book.category else [] 
    recommended_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:6] 
    is_favorite = False 
    if request.user.is_authenticated: 
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists() 
 
    # ── Discussion Groups ── 
    currently_reading_qs = ReadingStatus.objects.filter(book=book, status='reading').select_related('user') 
    already_read_qs      = ReadingStatus.objects.filter(book=book, status='read').select_related('user') 
    user_status = None 
    if request.user.is_authenticated: 
        try: 
            user_status = ReadingStatus.objects.get(user=request.user, book=book).status 
        except ReadingStatus.DoesNotExist: 
            pass 
 
    return render(request, 'book_detail.html', { 
        'book': book, 
        'avg_rating': round(avg_rating, 1), 
        'ratings_count': ratings_count, 
        'comments': comments, 
        'tags': tags, 
        'recommended_books': recommended_books, 
        'is_favorite': is_favorite, 
        'currently_reading_users': [r.user for r in currently_reading_qs], 
        'currently_reading_count': currently_reading_qs.count(), 
        'already_read_users':      [r.user for r in already_read_qs], 
        'already_read_count':      already_read_qs.count(), 
        'user_is_reading':         user_status == 'reading', 
        'user_has_read':           user_status == 'read', 
    }) 
 
 
# ========== API التفاعلات ========== 
@login_required 
def rate_book(request, book_id): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        book = get_object_or_404(Book, id=book_id) 
        Evaluation.objects.update_or_create( 
            user=request.user, book=book, 
            defaults={'note': data.get('rating')} 
        ) 
        new_avg = Evaluation.objects.filter(book=book).aggregate(avg=Avg('note'))['avg'] or 0 
        return JsonResponse({'success': True, 'avg_rating': round(new_avg, 1)}) 
    return JsonResponse({'success': False}) 
 
 
@login_required 
def add_to_favorite(request, book_id): 
    if request.method == 'POST': 
        book = get_object_or_404(Book, id=book_id) 
        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book) 
        if not created: 
            favorite.delete() 
            return JsonResponse({'success': True, 'added': False, 'message': 'Removed from My List'}) 
        return JsonResponse({'success': True, 'added': True, 'message': 'Added to My List'}) 
    return JsonResponse({'success': False}) 
 
 
@login_required 
def add_comment(request, book_id): 
    if request.method == 'POST': 
        data = json.loads(request.body) 
        content = data.get('content', '').strip() 
        if not content: 
            return JsonResponse({'success': False, 'error': 'Comment cannot be empty'}) 
        book = get_object_or_404(Book, id=book_id) 
        comment = Comment.objects.create(user=request.user, book=book, content=content) 
        return JsonResponse({ 
            'success': True, 
            'comment': { 
                'id': comment.id, 
                'user': comment.user.username, 
                'content': comment.content, 
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'likes_count': 0, 
            } 
        }) 
    return JsonResponse({'success': False}) 
 
 
@login_required 
def like_comment(request, comment_id): 
    if request.method == 'POST': 
        comment = get_object_or_404(Comment, id=comment_id) 
        like, created = Like.objects.get_or_create(user=request.user, comment=comment) 
        if not created: 
            like.delete() 
            return JsonResponse({'success': True, 'liked': False, 'likes_count': comment.likes.count()}) 
        return JsonResponse({'success': True, 'liked': True, 'likes_count': comment.likes.count()}) 
    return JsonResponse({'success': False}) 
def my_list(request): 
    if request.user.is_authenticated: 
        favorites = Favorite.objects.filter(user=request.user).select_related('book') 
        total_books = favorites.count() 
    else: 
        favorites = [] 
        total_books = 0 
    return render(request, 'my_list.html', { 
        'favorites': favorites, 
        'total_books': total_books, 
    }) 
 
 
# ========== Profile ========== 
@login_required 
def profile_view(request): 
    user = request.user 
    profile, _ = Profile.objects.get_or_create(user=user) 
 
    # avatar upload 
    if request.method == 'POST' and request.FILES.get('image'): 
        profile.image = request.FILES['image'] 
        profile.save() 
        return redirect('profile') 
 
    favorites      = Favorite.objects.filter(user=user).select_related('book') 
    total_favorites = favorites.count() 
    total_comments  = Comment.objects.filter(user=user).count() 
    total_ratings   = Evaluation.objects.filter(user=user).count() 
    reading_count   = ReadingStatus.objects.filter(user=user, status='reading').count() 
    read_count      = ReadingStatus.objects.filter(user=user, status='read').count() 
 
    return render(request, 'profile.html', { 
        'user'           : user, 
        'profile'        : profile, 
        'favorites'      : favorites, 
        'latest_favorites': favorites.order_by('-added_date')[:8], 
        'total_favorites': total_favorites, 
        'favorites_count': total_favorites, 
        'total_comments' : total_comments, 
        'comments_count' : total_comments, 
        'total_ratings'  : total_ratings, 
        'ratings_count'  : total_ratings, 
        'reading_count'  : reading_count, 
        'read_count'     : read_count, 
        'activity_score' : total_favorites + total_comments + total_ratings, 
    }) 
 

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name  = request.POST.get('last_name', '')
        new_username    = request.POST.get('username', user.username).strip()
        user.email      = request.POST.get('email', user.email)

        # تحقق من username فريد
        if new_username != user.username and User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user.username = new_username
            user.save()

            # gender
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.gender = request.POST.get('gender', profile.gender)
            profile.save()

            messages.success(request, 'Profile updated successfully!')

    return redirect('profile')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            update_session_auth_hash(request, form.save())
            messages.success(request, 'Password changed successfully!')
        else:
            # أرسل الأخطاء
            for error in form.errors.values():
                messages.error(request, error[0])
    return redirect('profile')


 
 
@login_required 
def delete_account(request): 
    request.user.delete() 
    return redirect('login') 
 
 
# ========== Notifications ========== 
@login_required 
def notifications_view(request): 
    notifications = Notification.objects.filter(user=request.user).order_by('-date') 
    unread_count = notifications.filter(is_read=False).count() 
    return render(request, 'notifications.html', {
       'notifications': notifications, 
        'unread_count': unread_count, 
    }) 
 
 
@login_required 
def mark_notification_read(request, notif_id): 
    if request.method == 'POST': 
        try: 
            notif = Notification.objects.get(id=notif_id, user=request.user) 
            notif.is_read = True 
            notif.save() 
            return JsonResponse({'success': True}) 
        except Notification.DoesNotExist: 
            return JsonResponse({'error': 'Not found'}, status=404) 
 
 
@login_required 
def mark_all_read(request): 
    if request.method == 'POST': 
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True) 
        return JsonResponse({'success': True}) 
 
 
@login_required 
def clear_all_notifications(request): 
    if request.method == 'POST': 
        Notification.objects.filter(user=request.user).delete() 
        return JsonResponse({'success': True}) 
 
 
# ========== Admin Dashboard ========== 
@staff_member_required 
def admin_dashboard(request): 
    return render(request, 'admin_dashboard.html', { 
        'total_books':      Book.objects.count(), 
        'total_users':      User.objects.count(), 
        'total_comments':   Comment.objects.count(), 
        'total_categories': Category.objects.count(), 
        'recent_users':     User.objects.order_by('-date_joined')[:5], 
        'recent_books':     Book.objects.order_by('-id')[:5], 
        'recent_comments':  Comment.objects.order_by('-created_at')[:5], 
        'categories':       Category.objects.all(), 
    }) 
@staff_member_required 
def ban_user(request, user_id): 
    if request.method == 'POST': 
        try: 
            user = User.objects.get(id=user_id) 
            user.is_active = not user.is_active 
            user.save() 
            return JsonResponse({'banned': not user.is_active}) 
        except User.DoesNotExist: 
            return JsonResponse({'error': 'Not found'}, status=404) 
 
 
@staff_member_required 
def delete_user(request, user_id): 
    if request.method == 'POST': 
        try: 
            User.objects.get(id=user_id).delete() 
            return JsonResponse({'success': True}) 
        except User.DoesNotExist: 
            return JsonResponse({'error': 'Not found'}, status=404) 
 
 
@staff_member_required 
def admin_delete_book(request, book_id): 
    if request.method == 'POST': 
        try: 
            Book.objects.get(id=book_id).delete() 
            return JsonResponse({'success': True}) 
        except Book.DoesNotExist: 
            return JsonResponse({'error': 'Not found'}, status=404) 
 
 
@staff_member_required 
def publish_book(request): 
    if request.method == 'POST': 
        book = Book( 
            title       = request.POST.get('title'), 
            author      = request.POST.get('author'), 
            description = request.POST.get('description', ''), 
        ) 
        if request.FILES.get('image'): 
            book.image = request.FILES['image'] 
        cat_id = request.POST.get('category') 
        if cat_id: 
            try: 
                book.category = Category.objects.get(id=cat_id) 
            except Category.DoesNotExist: 
                pass 
        book.save() 
        messages.success(request, 'Book published successfully!') 
    return redirect('admin_dashboard') 
 
 
 
def search_books(request): 
    """API للبحث عن الكتب""" 
    query = request.GET.get('q', '') 
    books = [] 
     
    if query and len(query) >= 2: 
        books_list = Book.objects.filter( 
            models.Q(title__icontains=query) | 
            models.Q(author__icontains=query) 
        )[:10] 
         
        for book in books_list: 
            books.append({ 
                'id': book.id, 
                'title': book.title, 
                'author': book.author, 
                'slug': slugify(book.title), 
                'image': book.image.url if book.image else None, 
            }) 
     
    return JsonResponse({'books': books})
 # ========== Discussion Groups ==========
@login_required
def join_group(request, book_id, group_type):
    if request.method == 'POST':
        if group_type not in ('reading', 'read'):
            return JsonResponse({'success': False}, status=400)
        book = get_object_or_404(Book, id=book_id)
        obj, created = ReadingStatus.objects.get_or_create(
            user=request.user,
            book=book,
            defaults={'status': group_type}
        )
        if not created:
            obj.status = group_type
            obj.save()
        return JsonResponse({'success': True, 'status': group_type})
    return JsonResponse({'success': False})


# ================================================================
#  أضف هذا في views.py
# ================================================================

@login_required
def group_chat(request, book_id, group_type):
    """صفحة chat الـ group — تفتح عند النقر على Join Group"""
    if group_type not in ('reading', 'read'):
        return redirect('home')

    book = get_object_or_404(Book, id=book_id)

    # تأكد أن المستخدم عضو في الـ group
    is_member = ReadingStatus.objects.filter(
        user=request.user, book=book, status=group_type
    ).exists()
    if not is_member:
        return redirect(f'/book/{slugify(book.title)}/')

    # كل الأعضاء
    members_qs = ReadingStatus.objects.filter(
        book=book, status=group_type
    ).select_related('user', 'user__profile')
    members = [rs.user for rs in members_qs]

    # الرسائل
    messages_list = GroupMessage.objects.filter(
        book=book, group_type=group_type
    ).select_related('user', 'user__profile')

    # أضف show_date لكل رسالة (لعرض فاصل التاريخ)
    prev_date = None
    for msg in messages_list:
        msg_date = msg.created_at.date()
        msg.show_date = (msg_date != prev_date)
        prev_date = msg_date

    last_msg = messages_list.last()

    return render(request, 'group_chat.html', {
        'book'             : book,
        'group_type'       : group_type,
        'group_type_display': 'Currently Reading' if group_type == 'reading' else 'Already Read',
        'members'          : members,
        'members_count'    : len(members),
        'messages_list'    : messages_list,
        'last_message_id'  : last_msg.id if last_msg else 0,
    })


@login_required
@require_POST
def send_group_message(request):
    """إرسال رسالة جديدة في الـ group"""
    data       = json.loads(request.body)
    book_id    = data.get('book_id')
    group_type = data.get('group_type')
    content    = data.get('content', '').strip()

    if not content or group_type not in ('reading', 'read'):
        return JsonResponse({'success': False})

    book = get_object_or_404(Book, id=book_id)

    # تأكد أن المستخدم عضو
    if not ReadingStatus.objects.filter(user=request.user, book=book, status=group_type).exists():
        return JsonResponse({'success': False, 'error': 'Not a member'})

    msg = GroupMessage.objects.create(
        book=book, user=request.user,
        group_type=group_type, content=content
    )

    # إرسال notification لبقية الأعضاء
    members = ReadingStatus.objects.filter(
        book=book, status=group_type
    ).exclude(user=request.user).select_related('user')

    for rs in members:
        Notification.objects.create(
            user      = rs.user,
            massage   = f'{request.user.username} sent a message in "{book.title}" group.',
            notif_type= 'group',
        )

    return JsonResponse({
        'success': True,
        'message': {
            'id'      : msg.id,
            'content' : msg.content,
            'username': request.user.username,
            'initial' : request.user.username[0].upper(),
            'time'    : msg.created_at.strftime('%H:%M'),
        }
    })
@login_required
def get_new_group_messages(request):
    """polling — جلب الرسائل الجديدة كل 8 ثوانٍ"""
    book_id    = request.GET.get('book_id')
    group_type = request.GET.get('group_type')
    last_id    = int(request.GET.get('last_id', 0))

    if not book_id or group_type not in ('reading', 'read'):
        return JsonResponse({'messages': []})

    new_msgs = GroupMessage.objects.filter(
        book_id=book_id, group_type=group_type, id__gt=last_id
    ).exclude(user=request.user).select_related('user')

    return JsonResponse({
        'messages': [
            {
                'id'      : m.id,
                'content' : m.content,
                'username': m.user.username,
                'initial' : m.user.username[0].upper(),
                'time'    : m.created_at.strftime('%H:%M'),
            }
            for m in new_msgs
        ]
    })

def logout(request):
    logout(request)
    return redirect('/')


@login_required
def my_groups(request):
    group_type = request.GET.get('type', 'reading')
    if group_type not in ('reading', 'read'):
        group_type = 'reading'

    statuses = ReadingStatus.objects.filter(
        user=request.user,
        status=group_type
    ).select_related('book', 'book__category')

    reading_count = ReadingStatus.objects.filter(user=request.user, status='reading').count()
    read_count    = ReadingStatus.objects.filter(user=request.user, status='read').count()

    return render(request, 'my_groups.html', {
        'statuses'     : statuses,
        'group_type'   : group_type,
        'reading_count': reading_count,
        'read_count'   : read_count,
    })

