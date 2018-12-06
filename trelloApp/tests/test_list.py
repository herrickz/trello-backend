from django.test import TestCase
from ..models import Board, List

class ListTest(TestCase):

    def test_delete_board_with_list_foreign_key_reference_deletes_list(self):
        board = Board.objects.create(name='board')
        trello_list = List.objects.create(name='trello list', board=board)

        board.delete()

        list_query_set = List.objects.filter(id=trello_list.id)

        self.assertEqual(len(list_query_set), 0)