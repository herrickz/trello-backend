from rest_framework import serializers
from .models import Board, List, Card

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'trelloList')

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class CreateCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'name', 'trelloList')

class ListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = List
        fields = '__all__'

class SingleBoardSerializer(serializers.ModelSerializer):
    lists = ListSerializer(many=True)

    class Meta:
        model = Board
        fields = '__all__'