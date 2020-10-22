from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', )

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'confirmation_code', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active', )

    fieldsets = (
        (
            None,
            {'fields': ('email', 'password', 'username', 'role')}
        ),
        (
            'Permissions',
            {'fields': ('is_admin',)}
        ),
        (
            'Access',
            {'fields': ('is_active', 'confirmation_code')}
        ),
        (
            'Credentials',
            {'fields': ('first_name', 'last_name', 'description')}
        ),
    )

    add_fieldsets = (
        (
            None,
            {'fields': ('email', 'password', 'username', 'role')}
        ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
