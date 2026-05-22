# your_app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from django.conf import settings

ADMIN_EMAIL = getattr(settings, 'ADMIN_EMAIL', 'adminaa1@gmail.com')

@receiver(post_save, sender=User)
def auto_make_admin(sender, instance, created, **kwargs):
    """
    Signal: عند حفظ مستخدم بالإيميل المحدد → تفعيل صلاحيات Admin تلقائياً
    """
    if instance.email.lower().strip() == ADMIN_EMAIL.lower().strip():
        updated = False
        
        if not instance.is_staff:
            instance.is_staff = True
            updated = True
        
        if not instance.is_superuser:
            instance.is_superuser = True
            updated = True
            
        if updated:
            instance.save(update_fields=['is_staff', 'is_superuser'])
        
        # إضافة لمجموعة Admins
        admin_group, _ = Group.objects.get_or_create(name='Admins')
        instance.groups.add(admin_group)