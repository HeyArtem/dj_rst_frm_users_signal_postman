from django.contrib import admin
from users_app.models import User, Profile

admin.site.register(Profile)

# поиск по полю "username"
@admin.register(User)
class UserAdmin(admin.ModelAdmin):    
    search_fields = ["username"]

