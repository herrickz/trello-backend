from django.shortcuts import render
from rest_framework import mixins, viewsets, status, serializers
from rest_framework.response import Response
from .serializers import BoardSerializer, ListSerializer, SingleBoardSerializer, CardSerializer
from .models import Board, List, Card
from django.core.serializers import serialize

import json

class BoardApi(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = BoardSerializer
    queryset = Board.objects.all()

    def retrieve(self, request, *args, **kwargs):
        
        board_hash_id = kwargs.get('pk')

        try:
            board = Board.objects.get(hashId=board_hash_id)

            board_serializer = SingleBoardSerializer(board)

            return Response(board_serializer.data)

        except Exception as exception:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

class BoardListApi(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ListSerializer
    queryset = List.objects.all()

class CardListApi(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CardSerializer
    queryset = Card.objects.all()