from django.contrib import admin
from .models import Post, GoTender, BuyTender, Person
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserCreationForm


class UserCreateForm(UserCreationForm):
    form = MyUserCreationForm
    class Meta:
        model = User
        fields = ('username', 'email')

class UserAdmins(UserAdmin):
    add_form = UserCreateForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1', 'password2', ),
        }),
    )



admin.site.unregister(User)
admin.site.register(User, UserAdmins)
admin.site.register(Person)
admin.site.register(Post)
admin.site.register(GoTender)
admin.site.register(BuyTender)