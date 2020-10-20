from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.core.exceptions import ValidationError

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Confimation code', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email',  'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active', )

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Access', {'fields': ('is_active',)}),
    )

    add_fieldsets = (
        (None, {
            'fields': ('email', 'password',),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
