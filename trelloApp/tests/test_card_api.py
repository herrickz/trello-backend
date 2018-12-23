from django.test import TestCase
from rest_framework import status
from ..models import Board, List, Card
from .converter import OrderedDictToObject
import json

class CardApiTest(TestCase):

    def test_get_all_cards_returns_1_card(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list, order=0)

        get_response = self.client.get('/api/card/')

        card = OrderedDictToObject(get_response.data[0])

        self.assertEqual(card.id, card_object.id)
        self.assertEqual(card.trelloList, trello_list.id)

    def test_get_single_card_returns_card(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list, order=0)

        get_response = self.client.get(f'/api/card/{card_object.id}/')

        card = OrderedDictToObject(get_response.data)

        self.assertEqual(card.id, card_object.id)
        self.assertEqual(card.trelloList, trello_list.id)

    def test_patch_card_with_updated_name_updates_name(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card_object = Card.objects.create(name='card', trelloList=trello_list, order=0)

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
        card_object = Card.objects.create(name='card', trelloList=trello_list, order=0)

        delete_response = self.client.delete(f'/api/card/{card_object.id}/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reorder_two_cards_in_same_list_where_first_card_is_dropped_in_position_1_updates_both_cards_orders(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)

        patch_card = {
            'id': first_card.id,
            'order': 1
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)

        self.assertEqual(updated_first_card.order, 1)
        self.assertEqual(updated_second_card.order, 0)

    def test_reorder_three_cards_in_same_list_where_first_card_is_dropped_in_position_2_updates_all_cards_orders(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)
        third_card = Card.objects.create(name='original third card', trelloList=trello_list, order=2)

        patch_card = {
            'id': first_card.id,
            'order': 2
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)
        updated_third_card = Card.objects.get(id=third_card.id)

        self.assertEqual(updated_second_card.order, 0)
        self.assertEqual(updated_third_card.order, 1)
        self.assertEqual(updated_first_card.order, 2)

    def test_reorder_four_cards_in_same_list_where_first_card_is_dropped_in_position_3_updates_all_cards_orders(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)
        third_card = Card.objects.create(name='original third card', trelloList=trello_list, order=2)
        fourth_card = Card.objects.create(name='original fourth card', trelloList=trello_list, order=3)

        patch_card = {
            'id': first_card.id,
            'order': 3
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)
        updated_third_card = Card.objects.get(id=third_card.id)
        updated_fourth_card = Card.objects.get(id=fourth_card.id)

        self.assertEqual(updated_second_card.order, 0)
        self.assertEqual(updated_third_card.order, 1)
        self.assertEqual(updated_fourth_card.order, 2)
        self.assertEqual(updated_first_card.order, 3)

    def test_reorder_four_cards_in_same_list_where_first_card_is_dropped_in_position_1_updates_only_affected_cards(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)
        third_card = Card.objects.create(name='original third card', trelloList=trello_list, order=2)
        fourth_card = Card.objects.create(name='original fourth card', trelloList=trello_list, order=3)

        patch_card = {
            'id': first_card.id,
            'order': 1
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)
        updated_third_card = Card.objects.get(id=third_card.id)
        updated_fourth_card = Card.objects.get(id=fourth_card.id)

        self.assertEqual(updated_second_card.order, 0)
        self.assertEqual(updated_first_card.order, 1)
        self.assertEqual(updated_third_card.order, 2)
        self.assertEqual(updated_fourth_card.order, 3)

    def test_reorder_three_cards_in_same_list_where_third_card_is_dropped_in_position_0_updates_all_cards_orders(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)
        third_card = Card.objects.create(name='original third card', trelloList=trello_list, order=2)

        patch_card = {
            'id': third_card.id,
            'order': 0
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)
        updated_third_card = Card.objects.get(id=third_card.id)

        self.assertEqual(updated_third_card.order, 0)
        self.assertEqual(updated_first_card.order, 1)
        self.assertEqual(updated_second_card.order, 2)

    def test_reorder_four_cards_in_same_list_where_fourth_card_is_dropped_in_position_0_updates_all_cards_orders(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)
        third_card = Card.objects.create(name='original third card', trelloList=trello_list, order=2)
        fourth_card = Card.objects.create(name='original fourth card', trelloList=trello_list, order=3)

        patch_card = {
            'id': fourth_card.id,
            'order': 0
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)
        updated_third_card = Card.objects.get(id=third_card.id)
        updated_fourth_card = Card.objects.get(id=fourth_card.id)

        self.assertEqual(updated_fourth_card.order, 0)
        self.assertEqual(updated_first_card.order, 1)
        self.assertEqual(updated_second_card.order, 2)
        self.assertEqual(updated_third_card.order, 3)

    def test_reorder_four_cards_in_same_list_where_second_card_is_dropped_in_position_3_updates_only_affected_cards(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        first_card = Card.objects.create(name='original first card', trelloList=trello_list, order=0)
        second_card = Card.objects.create(name='original second card', trelloList=trello_list, order=1)
        third_card = Card.objects.create(name='original third card', trelloList=trello_list, order=2)
        fourth_card = Card.objects.create(name='original fourth card', trelloList=trello_list, order=3)

        patch_card = {
            'id': second_card.id,
            'order': 3
        }

        patch_response = self.client.patch(f'/api/card/{first_card.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card.id)
        updated_second_card = Card.objects.get(id=second_card.id)
        updated_third_card = Card.objects.get(id=third_card.id)
        updated_fourth_card = Card.objects.get(id=fourth_card.id)

        self.assertEqual(updated_first_card.order, 0)
        self.assertEqual(updated_third_card.order, 1)
        self.assertEqual(updated_fourth_card.order, 2)
        self.assertEqual(updated_second_card.order, 3)

    def test_swap_card_from_list_one_length_one_to_list_two_length_zero_updates_lists_and_card_order(self):
        board = Board.objects.create(name='board')

        trello_list_one = List.objects.create(name='trello list one', board=board)
        trello_list_two = List.objects.create(name='trello list two', board=board)

        first_card_list_one = Card.objects.create(name='original first card', trelloList=trello_list_one, order=0)

        patch_card = {
            'id': first_card_list_one.id,
            'order': 0,
            'trelloList': trello_list_two.id
        }

        patch_response = self.client.patch(f'/api/card/{first_card_list_one.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card = Card.objects.get(id=first_card_list_one.id)

        self.assertEqual(updated_first_card.order, 0)
        self.assertEqual(updated_first_card.trelloList, trello_list_two)

    def test_swap_card_from_list_one_length_one_to_beginning_of_list_two_length_one_updates_lists_and_card_order(self):
        board = Board.objects.create(name='board')

        trello_list_one = List.objects.create(name='trello list one', board=board)
        trello_list_two = List.objects.create(name='trello list two', board=board)

        first_card_list_one = Card.objects.create(name='first card list one', trelloList=trello_list_one, order=0)
        first_card_list_two = Card.objects.create(name='first card list two', trelloList=trello_list_two, order=0)

        patch_card = {
            'id': first_card_list_one.id,
            'order': 0,
            'trelloList': trello_list_two.id
        }

        patch_response = self.client.patch(f'/api/card/{first_card_list_one.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card_list_one = Card.objects.get(id=first_card_list_one.id)
        updated_first_card_list_two = Card.objects.get(id=first_card_list_two.id)

        self.assertEqual(updated_first_card_list_one.order, 0)
        self.assertEqual(updated_first_card_list_one.trelloList, trello_list_two)

        self.assertEqual(updated_first_card_list_two.order, 1)

    def test_swap_card_from_list_one_length_one_to_beginning_of_list_two_length_three_updates_lists_and_card_order(self):
        board = Board.objects.create(name='board')

        trello_list_one = List.objects.create(name='trello list one', board=board)
        trello_list_two = List.objects.create(name='trello list two', board=board)

        first_card_list_one = Card.objects.create(name='first card list one', trelloList=trello_list_one, order=0)
        first_card_list_two = Card.objects.create(name='first card list two', trelloList=trello_list_two, order=0)
        second_card_list_two = Card.objects.create(name='second card list two', trelloList=trello_list_two, order=1)
        third_card_list_two = Card.objects.create(name='third card list two', trelloList=trello_list_two, order=2)

        patch_card = {
            'id': first_card_list_one.id,
            'order': 0,
            'trelloList': trello_list_two.id
        }

        patch_response = self.client.patch(f'/api/card/{first_card_list_one.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card_list_one = Card.objects.get(id=first_card_list_one.id)
        updated_first_card_list_two = Card.objects.get(id=first_card_list_two.id)
        updated_second_card_list_two = Card.objects.get(id=second_card_list_two.id)
        updated_third_card_list_two = Card.objects.get(id=third_card_list_two.id)

        self.assertEqual(updated_first_card_list_one.order, 0)
        self.assertEqual(updated_first_card_list_one.trelloList, trello_list_two)

        self.assertEqual(updated_first_card_list_two.order, 1)
        self.assertEqual(updated_second_card_list_two.order, 2)
        self.assertEqual(updated_third_card_list_two.order, 3)

    def test_swap_card_from_list_one_length_one_to_second_index_of_list_two_length_three_updates_lists_and_card_order(self):
        board = Board.objects.create(name='board')

        trello_list_one = List.objects.create(name='trello list one', board=board)
        trello_list_two = List.objects.create(name='trello list two', board=board)

        first_card_list_one = Card.objects.create(name='first card list one', trelloList=trello_list_one, order=0)
        first_card_list_two = Card.objects.create(name='first card list two', trelloList=trello_list_two, order=0)
        second_card_list_two = Card.objects.create(name='second card list two', trelloList=trello_list_two, order=1)
        third_card_list_two = Card.objects.create(name='third card list two', trelloList=trello_list_two, order=2)

        patch_card = {
            'id': first_card_list_one.id,
            'order': 1,
            'trelloList': trello_list_two.id
        }

        patch_response = self.client.patch(f'/api/card/{first_card_list_one.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card_list_one = Card.objects.get(id=first_card_list_one.id)
        updated_first_card_list_two = Card.objects.get(id=first_card_list_two.id)
        updated_second_card_list_two = Card.objects.get(id=second_card_list_two.id)
        updated_third_card_list_two = Card.objects.get(id=third_card_list_two.id)

        self.assertEqual(updated_first_card_list_one.order, 1)
        self.assertEqual(updated_first_card_list_one.trelloList, trello_list_two)

        self.assertEqual(updated_first_card_list_two.order, 0)
        self.assertEqual(updated_second_card_list_two.order, 2)
        self.assertEqual(updated_third_card_list_two.order, 3)

    def test_swap_card_from_list_one_length_one_to_last_index_of_list_two_length_three_updates_lists_and_card_order(self):
        board = Board.objects.create(name='board')

        trello_list_one = List.objects.create(name='trello list one', board=board)
        trello_list_two = List.objects.create(name='trello list two', board=board)

        first_card_list_one = Card.objects.create(name='first card list one', trelloList=trello_list_one, order=0)
        first_card_list_two = Card.objects.create(name='first card list two', trelloList=trello_list_two, order=0)
        second_card_list_two = Card.objects.create(name='second card list two', trelloList=trello_list_two, order=1)
        third_card_list_two = Card.objects.create(name='third card list two', trelloList=trello_list_two, order=2)

        patch_card = {
            'id': first_card_list_one.id,
            'order': 3,
            'trelloList': trello_list_two.id
        }

        patch_response = self.client.patch(f'/api/card/{first_card_list_one.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card_list_one = Card.objects.get(id=first_card_list_one.id)
        updated_first_card_list_two = Card.objects.get(id=first_card_list_two.id)
        updated_second_card_list_two = Card.objects.get(id=second_card_list_two.id)
        updated_third_card_list_two = Card.objects.get(id=third_card_list_two.id)

        self.assertEqual(updated_first_card_list_one.order, 3)
        self.assertEqual(updated_first_card_list_one.trelloList, trello_list_two)

        self.assertEqual(updated_first_card_list_two.order, 0)
        self.assertEqual(updated_second_card_list_two.order, 1)
        self.assertEqual(updated_third_card_list_two.order, 2)


    def test_swap_card_at_beginning_of_three_long_list_to_beginning_of_one_long_list_reorders_properly(self):
        board = Board.objects.create(name='board')

        trello_list_one = List.objects.create(name='trello list one', board=board)
        trello_list_two = List.objects.create(name='trello list two', board=board)

        first_card_list_one = Card.objects.create(name='original first card', trelloList=trello_list_one, order=0)
        second_card_list_one = Card.objects.create(name='original second card', trelloList=trello_list_one, order=1)
        third_card_list_one = Card.objects.create(name='original third card', trelloList=trello_list_one, order=2)

        first_card_list_two = Card.objects.create(name='original fourth card', trelloList=trello_list_two, order=0)

        patch_card = {
            'id': first_card_list_one.id,
            'order': 0,
            'trelloList': trello_list_two.id
        }

        patch_response = self.client.patch(f'/api/card/{first_card_list_one.id}/', data=json.dumps(patch_card), content_type='application/json')

        updated_first_card_list_one = Card.objects.get(id=first_card_list_one.id)
        updated_second_card_list_one = Card.objects.get(id=second_card_list_one.id)
        updated_third_card_list_one = Card.objects.get(id=third_card_list_one.id)

        updated_first_card_list_two = Card.objects.get(id=first_card_list_two.id)

        self.assertEqual(updated_first_card_list_one.order, 0)
        self.assertEqual(updated_first_card_list_one.trelloList, trello_list_two)

        self.assertEqual(updated_second_card_list_one.order, 0)
        self.assertEqual(updated_third_card_list_one.order, 1)

        self.assertEqual(updated_first_card_list_two.order, 1)