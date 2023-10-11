from django.contrib import admin
from .models import UavBrand, UavCategory, Uav


class UavAdmin(admin.ModelAdmin):
    search_fields = ("brand__manufacturer", "model", "category__category")
    list_display = ("brand", "model", "category")
    sortable_by = ("brand", "model", "category")


admin.site.register(Uav, UavAdmin)
admin.site.register(UavCategory)
admin.site.register(UavBrand)
