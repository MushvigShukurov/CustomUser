from PIL import Image
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email mutleqdir!")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.password = make_password(password=password)
        user.save()
        return user 
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True,verbose_name="Email")
    password = models.CharField(max_length=255,verbose_name="Şifrə")
    first_name = models.CharField(max_length=50,blank=True,null=True, verbose_name="Ad")
    last_name = models.CharField(max_length=50,blank=True,null=True, verbose_name="Soyad")
    avatar = models.ImageField(upload_to="profile/", blank=True, null=True, verbose_name="Profil Şəkli")

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)


    objects = CustomUserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name_plural = "İstifadəçilər"

    def __str__(self) -> str:
        return self.email
    
    def get_username(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def save(self,*args, **kvargs):
        self.password = make_password(self.password)
        super(CustomUser, self).save(*args,**kvargs)
        if self.avatar:
            image = Image.open(self.avatar.path)
            if image.width > 500 or image.height > 500:
                output_size = (500,500)
                image.thumbnail(output_size)
                image.save()

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, module):
        return True