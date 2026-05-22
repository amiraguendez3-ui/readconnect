# your_app/middleware.py
from django.shortcuts import redirect
from django.conf import settings

class AdminRedirectMiddleware:
    """
    Middleware: توجيه Admin تلقائياً من الصفحة الرئيسية إلى لوحة التحكم
    """
    
    def init(self, get_response):
        self.get_response = get_response
        self.admin_email = getattr(settings, 'ADMIN_EMAIL', 'adminaa1@gmail.com')
        
        # مسارات لا يتم توجيهها (منع loop)
        self.excluded_prefixes = [
            '/admin-dashboard',
            '/admin',
            '/login',
            '/logout',
            '/signup',
            '/static',
            '/media',
        ]

    def call(self, request):
        # التحقق من المسارات المستثناة أولاً
        if any(request.path.startswith(p) for p in self.excluded_prefixes):
            return self.get_response(request)
        
        # التحقق من المستخدم
        if (request.user.is_authenticated 
            and request.user.email == self.admin_email
            and request.user.is_staff):
            
            # توجيه فقط من الصفحة الرئيسية
            if request.path in ['/', '/home/']:
                return redirect('admin_dashboard')
        
        return self.get_response(request)