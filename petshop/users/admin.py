from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm
from .models import User, Address


class AddressInline(admin.StackedInline):
    model = Address


class UserModelAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'phone_number', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'is_superuser')
    readonly_fields = ('last_login',)

    fieldsets = (
        ('Main',
         {'fields':
             (
                 'username',
                 'email',
                 'phone_number',
                 'first_name',
                 'last_name',
                 'role',
                 'password',
                 'last_login'
             )
         }),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'groups', 'user_permissions')})
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password1', 'password2')}),
    )

    search_fields = ('email', 'username', 'phone_number')
    ordering = ('-created_date',)
    inlines = (AddressInline,)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.register(User, UserModelAdmin)


@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):
    list_display = ('owner__email', 'postal_code')
    search_fields = ('address',)
