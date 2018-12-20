from django.test import TestCase
from ..models import Board, List, Card
from django.db.utils import IntegrityError

class CardTest(TestCase):

    def test_delete_list_with_card_foreign_key_reference_deletes_card(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)
        card = Card.objects.create(name='card', trelloList=trello_list, order=0)

        trello_list.delete()

        card_query_set = Card.objects.filter(id=card.id)

        self.assertEqual(len(card_query_set), 0)


