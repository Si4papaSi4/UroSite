from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('bio/', views.bio, name='bio'),
    path('reviews/', views.reviews, name='reviews'),

    path('articles/<int:pk>/', views.article_detail_view,
         name='article_detail'),
    path('submit_review/', views.submit_review, name='submit_review'),
]
