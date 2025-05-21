from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from receipts.models import Store, UserProfile
from django.contrib.auth.models import User

# Register your models here.
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Store Assignment'

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class StoreAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.userprofile.store.id)

admin.site.register(Store, StoreAdmin)