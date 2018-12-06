from django.test import TestCase
from rest_framework import status
from ..models import Board, List, Card
from .converter import OrderedDictToObject
import json

class CardApiTest(TestCase):

    def test_get_all_cards_returns_1_card(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list)

        get_response = self.client.get('/api/card/')

        card = OrderedDictToObject(get_response.data[0])

        self.assertEqual(card.id, card_object.id)
        self.assertEqual(card.trelloList, trello_list.id)

    def test_get_single_card_returns_card(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list)

        get_response = self.client.get(f'/api/card/{card_object.id}/')

        card = OrderedDictToObject(get_response.data)

        self.assertEqual(card.id, card_object.id)
        self.assertEqual(card.trelloList, trello_list.id)

    def test_put_card_updates_card_name_and_trello_list_reference(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list)

        updated_trello_list = List.objects.create(name='updated trello list', board=board)

        put_card = {
            'id': card_object.id,
            'name': 'updated card name',
            'trelloList': updated_trello_list.id
        }

        put_response = self.client.put(f'/api/card/{card_object.id}/', data=json.dumps(put_card), content_type='application/json')

        card = OrderedDictToObject(put_response.data)

        self.assertEqual(card.name, 'updated card name')
        self.assertEqual(card.trelloList, updated_trello_list.id)

    # patch
    def test_patch_card_with_updated_name_updates_name(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list)

        patch_card = {
            'id': card_object.id,
            'name': 'updated card name',
        }

        patch_response = self.client.patch(f'/api/card/{card_object.id}/', data=json.dumps(patch_card), content_type='application/json')

        card = OrderedDictToObject(patch_response.data)

        self.assertEqual(card.name, 'updated card name')
    
    def test_delete_card_deletes_card(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list)

        delete_response = self.client.delete(f'/api/card/{card_object.id}/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)