from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from .models import Book, Category, Comment, Evaluation, Favorite, Like
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import Coalesce
from django.db.models import Value, FloatField, F
from django.contrib.auth.models import User
import json

# ========== الصفحة الرئيسية ==========
def home(request):
    # آخر 8 كتب أضيفت
    new_books = Book.objects.order_by('-created_at')[:8]

    # أفضل 8 كتب حسب متوسط التقييم
    best_books = Book.objects.annotate(
        avg_note=Coalesce(
            Avg('evaluations__note'),
            Value(0.0),
            output_field=FloatField()
        )
    ).order_by('-avg_note')[:8]
    
    trending_books = Book.objects.annotate(
        total_favorites=Count('favorite'),
        total_likes=Count('comments__likes'),
        total_comments=Count('comments'),
        total_evaluations=Count('evaluations'),
        trending_score=
            F('total_likes') * 2 +
            F('total_comments') * 3 +
            F('total_evaluations') * 1 +
            F('total_favorites') * 2
    ).order_by('-trending_score')[:8]
        
    top_users = User.objects.annotate(
        total_interactions=(
            Count('comments') + 
            Count('likes') + 
            Count('evaluations') + 
            Count('favorites')
        )
    ).order_by('-total_interactions')[:8]
    
    return render(request, 'home.html', {
        'new_books': new_books,
        'best_books': best_books,
        'trending_books': trending_books,
        'top_users': top_users
    })

# ========== صفحات التسجيل والدخول ==========
def signup(request):
    return render(request, 'signup.html')

def login_views(request):
    return render(request, 'login.html')

# ========== صفحات التصنيفات ==========
def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    books = Book.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'category_books.html', {
        'category': category,
        'books': books,
        'categories': categories
    })

def explore(request):
    one_week_ago = timezone.now() - timedelta(days=7)
    new_books = Book.objects.filter(created_at__gte=one_week_ago).order_by('-created_at')
    popular_books = Book.objects.order_by('-likes')[:10]
    return render(request, 'explore.html', {
        'new_books': new_books,
        'popular_books': popular_books
    })

def categories_view(request):
    categories = Category.objects.all()
    
    icons_map = {
        'arts': '📷', 'fiction': '📖', 'romance': '💖', 'food': '🍔',
        'health': '🩺', 'selfhelp': '💡', 'science': '🧪', 'biography': '📝',
        'business': '📊', 'history': '🏛️', 'thriller': '🔪', 'children': '🧸',
        'scifi': '🚀', 'outdoors': '🌿', 'sports': '⚽️', 'travel': '🗺️',
        'comics': '💥', 'poetry': '✒️', 'religion': '✝️',
    }
    
    categories_with_books = []
    total_books = 0
    
    for category in categories:
        books = category.book_set.all()[:6]
        category_name = category.name.lower()
        book_count = category.book_set.count()
        total_books += book_count
        
        categories_with_books.append({
            'id': category.id,
            'name': category.name,
            'title': category.name.capitalize(),
            'icon': icons_map.get(category_name, '📚'),
            'books': books,
            'book_count': book_count,
        })
    
    return render(request, 'categories.html', {
        'categories_with_books': categories_with_books,
        'total_books': total_books,
    })

def category_detail(request, name):
    return render(request, "category_detail.html", {"name": name})
# ========== صفحة تفاصيل الكتاب ==========
def book_detail(request, slug):
    # البحث عن الكتاب
    book = get_object_or_404(Book, title__iexact=slug.replace('-', ' '))
    
    # حساب متوسط التقييمات
    avg_rating_data = Evaluation.objects.filter(book=book).aggregate(avg=Avg('note'))
    avg_rating = avg_rating_data['avg'] or 0
    ratings_count = Evaluation.objects.filter(book=book).count()
    
    # جلب التعليقات مع عدد الإعجابات لكل تعليق
    comments = book.comments.all().annotate(likes_count=Count('likes')).order_by('-created_at')
    
    # التصنيفات للـ tags
    tags = [book.category.name] if book.category else []
    
    # كتب مقترحة من نفس التصنيف
    recommended_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:6]
    
    # التحقق إذا كان الكتاب في قائمة المفضلة للمستخدم الحالي
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    
    return render(request, 'book_detail.html', {
        'book': book,
        'avg_rating': round(avg_rating, 1),
        'ratings_count': ratings_count,
        'comments': comments,
        'tags': tags,
        'recommended_books': recommended_books,
        'is_favorite': is_favorite,
    })

# ========== API للتفاعلات ==========
@login_required
def rate_book(request, book_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data.get('rating')
        book = get_object_or_404(Book, id=book_id)
        
        evaluation, created = Evaluation.objects.update_or_create(
            user=request.user,
            book=book,
            defaults={'note': rating}
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
        content = data.get('content')
        book = get_object_or_404(Book, id=book_id)
        
        comment = Comment.objects.create(
            user=request.user,
            book=book,
            content=content
        )
        
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'user': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'likes_count': 0
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
            likes_count = comment.likes.count()
            return JsonResponse({'success': True, 'liked': False, 'likes_count': likes_count})
        
        likes_count = comment.likes.count()
        return JsonResponse({'success': True, 'liked': True, 'likes_count': likes_count})
    return JsonResponse({'success': False})
 

def my_list(request):
    """صفحة عرض الكتب المفضلة للمستخدم"""
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