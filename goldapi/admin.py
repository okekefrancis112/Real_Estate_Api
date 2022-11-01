from django.contrib import admin
from .models import Realtor,Property

class RealtorAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists()


    def save_model(self, request, obj, form, change):
        if obj.referral is None:
            obj.referral = obj.referral
            super(RealtorAdmin, self).save_model(request, obj, form, change)
        else:
            super(RealtorAdmin, self).save_model(request, obj, form, change)


class PropertyAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists()


    def save_model(self, request, obj, form, change):
        if obj.referral is None:
            obj.referral = obj.referral
            super(PropertyAdmin, self).save_model(request, obj, form, change)
        else:
            super(PropertyAdmin, self).save_model(request, obj, form, change)

admin.site.register(Realtor,RealtorAdmin)
admin.site.register(Property,PropertyAdmin)
