from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users_app.managers import MyAccountManager
from djoser.signals import user_registered
from django.dispatch import receiver
from django.core.validators import RegexValidator #Валидатор регулярных выражений


class User(AbstractBaseUser, PermissionsMixin):
    # [RegexValidator('^[a-z0-9_-]{3,15}$')] - регу.выраж. разрешает вводить имя пользователя символы от a-z и от 0-9 и "-" нижнего региствра, длина от 3 до 15
    username = models.CharField(verbose_name="Name user", max_length=25, unique=True, validators=[RegexValidator('^[a-z0-9_-]{3,15}$')])
    email = models.EmailField(verbose_name='Email user', max_length=40, unique=True)
    date_joined = models.DateTimeField(verbose_name='registration date', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='date of last visit', auto_now=True)
    # временно выставил default=True, в дальнейшем, напишу код, который будет менять статус пользователю после подтверждения email
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # имя пользователя изменил с email на username
    USERNAME_FIELD = 'username'
    
    # поля обязательные для заполнения
    REQUIRED_FIELDS = ['email']
    
    # менеджер моделей, у него будет несколько функции
    objects = MyAccountManager()
    
    # магич метод для админки
    def __str__(self) -> str:
        return f"{self.username} - {self.email}"
    
    # при удалении пользователя, инфа о нем будет храниться с пометкой is_activ = False
    def delete(self):
        self.is_active = False
        self.save()
        
        
#  Эта модель расширяет первоначальную модель User. При создании пользователя, автоматически будет создаваться Profile(добавится avatar & bio)
# это происходит за счет сигнала
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to="users_avatars", default="default_avatars/default_avatar.jpg")
    bio = models.CharField(max_length=500)
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
        
    def __str__(self) -> str:
        return self.user.username
    

# сигнал (реакция) на регистрацию пользователя
@receiver(user_registered)
def create_profile(user, **kwargs):
    Profile.objects.create(user=user)
