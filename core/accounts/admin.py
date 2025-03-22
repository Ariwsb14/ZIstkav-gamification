from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , Profile
# Register your models here.

        

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email' ,'is_superuser','is_active', 'is_staff')
    list_filter = ('email' , 'is_superuser','is_active', 'is_staff')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ('user Auth infos',{
            "fields":(
                'email','password'
            )
        }),
        ('premissions',{
            "fields":(
                'is_staff','is_active','is_superuser'
            )
        }),
        ('group premissions',{
            "fields":(
                'groups','user_permissions'
            )
        }),
        ('important dates',{
            "fields":(
                'last_login','expir_date'
            )
        }),
    )
    add_fieldsets =(
        ('Create User',{
            "fields":(
                'email','password1','password2','is_staff','is_active','is_superuser'
            )
        }),
    )

admin.site.register(Profile)
admin.site.register(User,CustomUserAdmin)
