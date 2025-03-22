from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import datetime
# Create your models here.

'''
Custum UserManger  for User MOdel
'''
class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError(_('Email must be provided'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))

       
        
        return self.create_user(email, password, **extra_fields)

'''
define CustomUser model for app with a unique email field and usermanager
'''
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250,unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    expir_date = models.DateTimeField(blank=True, null=True)
    updated_date = models.DateTimeField(auto_now=True)

    # set email as a username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # set user manager
    objects = UserManager()

    def is_expired(self):
        return self.expir_date < timezone.now()
    def save(self, *args, **kwargs):
        if not self.expir_date:
            self.expir_date = self.created_date + datetime.timedelta(days=30)
        if self.is_expired():
            self.is_active = False
        else:
            self.is_active = True
        
        super().save(*args, **kwargs)
    # return user email as a user model name 
    def __str__(self):
        return self.email


'''
user profile model
'''
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    # chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    # game = models.ForeignKey(Game, on_delete=models.CASCADE)
    ranks = (
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('diamond', 'Diamond'),
    )
    rank = models.CharField(default = ranks[0] , max_length=255, choices=ranks)
    xp = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def rank_calculate(self):
        ranks = ['bronze','silver','gold','platinum','diamond']
        if self.xp >= 10000 and self.rank != 'diamond':
            self.xp = self.xp - 10000
            self.rank = ranks[ranks.index(self.rank) + 1]
    def save(self, *args, **kwargs):
        self.rank_calculate()  # Call rank_calculate before saving
        super().save(*args, **kwargs)
    def __str__(self):
        return f'{self.user.email} Profile'


'''
signal to create profile when user is created
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)