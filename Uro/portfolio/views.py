from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import Article, Review


def home(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})


def bio(request):
    return render(request, 'bio.html')


def reviews(request):
    reviews = Review.objects.all().order_by('order')

    if request.method == 'POST':  # Если пользователь отправил форму
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Отзыв успешно отправлен!")
            return redirect('reviews')  # Перезагружаем страницу, чтобы избежать повторной отправки формы
    else:
        form = ReviewForm()

    return render(request, 'reviews.html', {'reviews': reviews, 'form': form})


def article_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    # благодаря related_name='images' получаем картинки так:
    images = article.images.all()
    return render(request, 'article_detail.html', {
        'article': article,
        'images': images
    })


from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render

from .forms import ReviewForm
from .models import Review


def submit_review(request):
    reviews = Review.objects.all().order_by('order')

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Ваш отзыв успешно отправлен!")

            # Теперь редирект сохраняет сообщения!
            return redirect("reviews")  # Не нужно вручную дописывать `#review-form`

        else:
            messages.error(request, "❌ Ошибка! Проверьте введенные данные.")

            # Если AJAX, отправляем ошибки в JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    "success": False,
                    "message": "❌ Ошибка! Проверьте введенные данные.",
                    "errors": form.errors
                })

    else:
        form = ReviewForm()

    return render(request, "reviews.html", {"reviews": reviews, "form": form})