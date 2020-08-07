from django.shortcuts import render
from rest_framework import generics,permissions
from .models import *
from .serializers import *
from .service import get_client_ip,MovieFilter
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

class MovieList(generics.ListAPIView):
    serializer_class = MovieRest
    filter_backends = (DjangoFilterBackend,)
    filterset_class=MovieFilter
    #permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=(models.Avg("ratings__star"))
        )
        return movies


class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailRest


class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewRest


class AddRating(generics.CreateAPIView):
    serializer_class = CreateRatingRest
    def perform_create(self, serializer):    #Дополнение к save
        serializer.save(ip=get_client_ip(self.request))

class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListRest


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailRest
