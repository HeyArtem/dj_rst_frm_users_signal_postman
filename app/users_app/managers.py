from django.contrib.auth.models import BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, username, password, email):
        # проверка на наличие username
        if not username:
            raise ValueError('Пользователь должен иметь username')
        
        # формирую user
        user = self.model(
            username=username,
            email=self.normalize_email(email=email)
        ) # normalize_email проверка валидности емейла
        user.set_password(password)
        user.save(using=self._db) # сохраняю пользователя
        
        return user
    
    
    def create_superuser(self, username, password, email):
        user = self.create_user(
            email=self.normalize_email(email=email),
            username=username,
            password=password
        )
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        
        return user
