from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class MovieList(APIView):
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
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
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        serializer = CreateRatingRest(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=self.get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
