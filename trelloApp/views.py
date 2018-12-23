from django.shortcuts import render
from rest_framework import mixins, viewsets, status, serializers
from rest_framework.response import Response
from .serializers import BoardSerializer, ListSerializer, SingleBoardSerializer, CardSerializer, CreateCardSerializer
from .models import Board, List, Card
from django.core.serializers import serialize

from django.db import transaction

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

class ListApi(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ListSerializer
    queryset = List.objects.all()

class CardApi(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = CardSerializer
    queryset = Card.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCardSerializer
        else:
            return CardSerializer
        
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):

        if('order' in request.data):
            
            card_id = request.data['id']
            new_order_number = request.data['order']

            if 'trelloList' in request.data:
                card = Card.objects.get(id=card_id)

                old_list_id = card.trelloList.id
                new_list_id = request.data['trelloList']

                if old_list_id != new_list_id:
                    return self.reorder_cards_in_different_lists(card_id, new_list_id, new_order_number)
                else:
                    return self.reorder_cards_in_same_list(card_id, new_order_number)
                    
            else:
                return self.reorder_cards_in_same_list(card_id, new_order_number)


        return super().update(request, *args, **kwargs)

    def reorder_cards_in_same_list(self, card_id, new_order_number):
        old_card_object = Card.objects.get(id=card_id)

        starting_index = min(old_card_object.order, new_order_number)
        ending_index = max(old_card_object.order, new_order_number)

        all_cards_in_order = old_card_object.trelloList.cards.all().order_by('order')
        cards_to_update = list(all_cards_in_order[starting_index:ending_index + 1])

        cards_to_update_in_order_of_new_order = []
        
        old_order_number = old_card_object.order

        if new_order_number > old_order_number:
            cards_to_update_in_order_of_new_order.append(old_card_object)
            
            for card in reversed(cards_to_update):
                if card.id != old_card_object.id:
                    cards_to_update_in_order_of_new_order.insert(0, card)

        else:
            cards_to_update_in_order_of_new_order.append(old_card_object)

            for card in cards_to_update:
                if card.id != old_card_object.id:
                    cards_to_update_in_order_of_new_order.append(card)

        last_order_number = all_cards_in_order.last().order
        
        with transaction.atomic():
            
            self.update_cards_to_update_to_new_order(last_order_number, cards_to_update_in_order_of_new_order)

            actual_order_number = starting_index

            for card in cards_to_update_in_order_of_new_order:
                card.order = actual_order_number
                card.save()

                actual_order_number += 1
        
        return Response(CardSerializer(old_card_object).data)

    def reorder_cards_in_different_lists(self, card_id, new_list_id, new_order):

        old_card = Card.objects.get(id=card_id)
        old_card_order = old_card.order 

        old_card_list = old_card.trelloList
        new_card_list = List.objects.get(id=new_list_id)

        with transaction.atomic():
            
            if len(new_card_list.cards.all()) == 0:
                self.update_old_card(new_card_list, old_card, 0)
            else:
                self.update_new_list(new_card_list, new_order, old_card)

            if len(old_card_list.cards.all()) != 0:
                self.update_old_list(old_card_list, old_card_order)

        return Response(CardSerializer(old_card).data)

    def update_old_list(self, old_card_list, old_card_order):
        all_cards_in_order = old_card_list.cards.all().order_by('order')
        cards_to_update = list(all_cards_in_order[old_card_order:])

        updated_order = old_card_order

        for card in cards_to_update:
            card.order = updated_order
            card.save()

            updated_order += 1

    def update_new_list(self, new_card_list, new_order, old_card):
        all_cards_in_order = new_card_list.cards.all().order_by('order')
        cards_to_update = list(all_cards_in_order[new_order:])

        if len(cards_to_update) == 0:
            self.update_old_card(new_card_list, old_card, new_order)

        else:
            self.push_cards_to_update_to_back(all_cards_in_order, cards_to_update)

            self.update_old_card(new_card_list, old_card, new_order)

            self.update_cards_to_update_to_new_order(new_order, cards_to_update)

    def update_cards_to_update_to_new_order(self, new_order, cards_to_update):
        card_update_order = new_order + 1

        for card in cards_to_update:
            card.order = card_update_order
            card.save()

            card_update_order += 1

    def push_cards_to_update_to_back(self, all_cards_in_order, cards_to_update):
        last_order_number = all_cards_in_order.last().order

        self.update_cards_to_update_to_new_order(last_order_number, cards_to_update)

    def update_old_card(self, new_card_list, old_card, new_order):
        old_card.trelloList = new_card_list
        old_card.order = new_order
        old_card.save()
        