from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, ConfirmationCode


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ('email', 'phone_number', 'is_active', 'is_staff')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone_number',)}),
        ('Permissions', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'phone_number',
                'password1',
                'password2',
                'is_active',
                'is_staff'
            ),
        }),
    )

    search_fields = ('email',)
    filter_horizontal = ('groups', 'user_permissions')


@admin.register(ConfirmationCode)
class ConfirmationCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at')