from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import *
from .models import Actor

class ActorViewSet(viewsets.ViewSet):
    def list(self,request):
        queryset=Actor.objects.all()
        serializer=ActorListRest(queryset,many=True)
        return Response(serializer.data)
    def retrieve(self,request,pk=None):
        queryset=Actor.objects.all()
        actor=get_object_or_404(queryset,pk=pk)
        serializer=ActorDetailRest(actor)
        return Response(serializer.data)

