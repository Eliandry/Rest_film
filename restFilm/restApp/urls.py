from . import views
from django.urls import path, include

urlpatterns = [
    path('movie/',views.MovieList.as_view()),
    path('movie/<int:pk>/',views.MovieDetail.as_view()),
    path('review/',views.ReviewCreate.as_view()),
    path('rating/',views.AddRating.as_view()),

]