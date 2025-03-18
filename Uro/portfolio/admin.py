from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import mark_safe

from .models import Article, ArticleImage, Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone', 'content')
    search_fields = ('first_name', 'last_name', 'phone')

# Убираем группы из админки
admin.site.unregister(Group)

# Настройка заголовков админки
admin.site.site_header = "Административная панель"
admin.site.site_title = "Админка"
admin.site.index_title = "Добро пожаловать в административную панель"

# Инлайн для дополнительных изображений
class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1
    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview', 'caption', 'order')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img src="{obj.image.url}" style="max-height: 100px;">')
        return "Нет изображения"

    image_preview.short_description = "Предпросмотр"

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_preview')
    readonly_fields = ('image_preview',)
    inlines = [ArticleImageInline]  # Определим ниже ArticleImageInline

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;">')
        return "Нет изображения"
    image_preview.short_description = "Предпросмотр изображения"
