import re

from django.core.exceptions import ValidationError
from django.core.validators import (MaxLengthValidator, MinLengthValidator,
                                    RegexValidator)
from django.db import models


# Валидатор для проверки, что поле содержит только буквы, пробелы и дефисы.
def validate_alpha(value):
    if not re.match(r'^[a-zA-Zа-яА-ЯёЁ\s\-]+$', value):
        raise ValidationError('Поле должно содержать только буквы, пробелы или дефисы.')

# Валидатор для номера телефона (пример: от 9 до 15 цифр, опционально начинается с +)
phone_validator = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Введите правильный номер телефона. Номер должен содержать от 9 до 15 цифр и может начинаться с +."
)

class Review(models.Model):
    first_name = models.CharField(
        "Имя",
        max_length=100,
        validators=[validate_alpha],
        help_text="Введите имя, используя только буквы, пробелы или дефисы."
    )
    last_name = models.CharField(
        "Фамилия",
        max_length=100,
        validators=[validate_alpha],
        help_text="Введите фамилию, используя только буквы, пробелы или дефисы."
    )
    phone = models.CharField(
        "Номер телефона",
        max_length=50,
        unique=True,
        validators=[phone_validator],
        help_text="Введите номер телефона (от 9 до 15 цифр, может начинаться с +)."
    )
    content = models.TextField(
        "Отзыв",
        validators=[
            MinLengthValidator(10, "Отзыв должен быть не менее 10 символов."),
            MaxLengthValidator(1000,
                               "Отзыв не должен превышать 1000 символов.")
        ],
        help_text="Введите ваш отзыв (не менее 10 символов)."
    )
    order = models.PositiveIntegerField("Порядок", default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"

    class Meta:
        ordering = ['order']
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Article(models.Model):
    title = models.CharField("Название", max_length=50)
    content = models.TextField("Содержание")
    image = models.ImageField("Главная картинка", upload_to='articles/',
                              blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"


class ArticleImage(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Статья"
    )
    image = models.ImageField("Изображение", upload_to='article_images/')
    caption = models.CharField("Подпись", max_length=255, blank=True,
                               null=True)
    order = models.PositiveIntegerField("Порядок", default=0)

    class Meta:
        ordering = ['order']
        verbose_name = "Дополнительное изображение"
        verbose_name_plural = "Дополнительные изображения"

    def __str__(self):
        return f"Изображение для {self.article.title}"
