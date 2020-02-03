from django.contrib import admin
from .models import LikeCount
# Register your models here.
@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id',)