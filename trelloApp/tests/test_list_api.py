from django.test import TestCase
from rest_framework import status
from ..models import Board, List, Card
import json
from collections import OrderedDict
from .converter import OrderedDictToObject

class ListApiTest(TestCase):

    def test_get_all_lists_returns_single_list(self):

        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)

        get_response = self.client.get('/api/list/')
        trello_list = OrderedDictToObject(get_response.data[0])
        
        self.assertEqual(trello_list.id, trello_list_object.id)
        self.assertEqual(trello_list.name, 'test list')
        self.assertEqual(trello_list.board, board.id)

    def test_get_board_with_single_card(self):

        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)
        card = Card.objects.create(name='test card', trelloList=trello_list_object)

        get_response = self.client.get('/api/list/')
        trello_list = OrderedDictToObject(get_response.data[0])

        self.assertEqual(trello_list.cards[0].id, card.id)
        self.assertEqual(trello_list.id, trello_list_object.id)
        self.assertEqual(trello_list.name, trello_list_object.name)

