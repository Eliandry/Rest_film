from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from .service import get_client_ip
from django.db import models

class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings',filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            middle_star=(models.Avg("ratings__star"))
        )
        serializer = MovieRest(movies, many=True)
        return Response(serializer.data)


class MovieDetail(APIView):
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailRest(movie)
        return Response(serializer.data)


class ReviewCreate(APIView):
    def post(self, request):
        review = ReviewRest(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddRating(APIView):


    def post(self, request):
        serializer = CreateRatingRest(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListRest

class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailRest