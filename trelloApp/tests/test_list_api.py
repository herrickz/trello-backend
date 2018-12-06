from django.test import TestCase
from rest_framework import status
from ..models import Board, List, Card
import json
from collections import OrderedDict
from .converter import OrderedDictToObject

class ListApiTest(TestCase):

    def test_get_all_lists_with_single_card(self):

        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)
        card = Card.objects.create(name='test card', trelloList=trello_list_object)

        get_response = self.client.get('/api/list/')
        trello_list = OrderedDictToObject(get_response.data[0])

        self.assertEqual(trello_list.cards[0].id, card.id)
        self.assertEqual(trello_list.id, trello_list_object.id)
        self.assertEqual(trello_list.name, trello_list_object.name)

    def test_get_single_list_returns_list(self):
        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)

        get_response = self.client.get(f'/api/list/{trello_list_object.id}/')
        trello_list = OrderedDictToObject(get_response.data)

        self.assertEqual(trello_list.id, trello_list_object.id)
        self.assertEqual(trello_list.name, trello_list_object.name)
        self.assertEqual(trello_list.board, board.id)

    def test_put_list_with_new_board_and_name_updates_list(self):
        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)

        updated_board = Board.objects.create(name='updated board')

        put_list = {
            'id': trello_list_object.id,
            'name': 'updated list name',
            'board': updated_board.id
        }

        put_response = self.client.put(f'/api/list/{trello_list_object.id}/', data=json.dumps(put_list), content_type='application/json')

        trello_list = OrderedDictToObject(put_response.data)

        self.assertEqual(trello_list.name, 'updated list name')
        self.assertEqual(trello_list.board, updated_board.id)

    def test_patch_list_with_new_name_updates_list(self):
        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)

        updated_board = Board.objects.create(name='updated board')

        patch_list = {
            'id': trello_list_object.id,
            'name': 'updated list name',
        }

        patch_response = self.client.patch(f'/api/list/{trello_list_object.id}/', data=json.dumps(patch_list), content_type='application/json')

        trello_list = OrderedDictToObject(patch_response.data)

        self.assertEqual(trello_list.name, 'updated list name')

    def test_delete_list_deletes_list(self):
        board = Board.objects.create(name='test board')
        trello_list_object = List.objects.create(name='test list', board=board)

        delete_response = self.client.delete(f'/api/list/{trello_list_object.id}/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
