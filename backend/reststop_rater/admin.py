# /backend/reststop_rater/admin.py

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models.bathroom import Bathroom
from .models.review import Review

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0

class BathroomAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'rating', 'created_at', 'updated_at')
    search_fields = ('name', 'address')
    inlines = [ReviewInline]
    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for bathroom in queryset:
            bathroom.reviews.all().delete()
            bathroom.delete()
        self.message_user(request, "Selected bathrooms and their reviews have been deleted.")
    delete_selected.short_description = "Delete selected bathrooms and reviews"

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('bathroom', 'user', 'rating', 'created_at', 'updated_at')
    search_fields = ('user__username', 'bathroom__name')

# Register the models and their admin classes
admin.site.register(Bathroom, BathroomAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
