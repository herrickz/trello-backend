from django.test import TestCase
from rest_framework import status
from ..models import Board, List
import json

class Test(TestCase):

    def test_get_board_with_hashid_returns_board(self):

        board = Board.objects.create(name='board test')
        
        get_response = self.client.get(f'/api/board/{board.hashId}/')

        self.assertEqual(get_response.data['id'], 1)
        self.assertEqual(get_response.data['name'], 'board test')
        self.assertEqual(get_response.data['hashId'], board.hashId)

    def test_get_board_with_list_returns_board_and_list(self):
        board = Board.objects.create(name='board test')
        trello_list = List.objects.create(name='test list', board=board)
        
        get_response = self.client.get(f'/api/board/{board.hashId}/')
        
        trello_list = get_response.data['lists'][0]

        self.assertEqual(trello_list['name'], 'test list')
        self.assertEqual(trello_list['board'], board.id)

    def test_retrieve_cannot_find_board_returns_HTTP_404(self):
        
        not_found_hash_id = 'notfoundhash'
        not_found_board = self.client.get(f'/api/board/{not_found_hash_id}/')

        self.assertEqual(not_found_board.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_board_creates_board(self):
        
        post_response = self.client.post('/api/board/', json.dumps({ 'name': 'test board' }), content_type='application/json')

        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(post_response.data['id'], 1)
        self.assertEqual(post_response.data['name'], 'test board')

    def test_patch_board_name_updates_board(self):
        board = Board.objects.create(name='board test')

        patch_board = {
            'id': board.id,
            'name': 'updated board name'
        }

        patch_response = self.client.patch(f'/api/board/{board.id}/', data=json.dumps(patch_board), content_type='application/json')

        self.assertEqual(patch_response.data['name'], 'updated board name')

    def test_put_board_with_updated_hashId_returns_original_hashId(self):
        board = Board.objects.create(name='board')

        put_board = {
            'id': board.id,
            'name': 'updated board name',
            'hashId': 'trying to update hash'
        }

        put_response = self.client.put(f'/api/board/{board.id}/', data=json.dumps(put_board), content_type='application/json')

        self.assertEqual(put_response.data['hashId'], board.hashId)

    def test_delete_board_successfully_deletes(self):
        board = Board.objects.create(name='board to delete')

        delete_response = self.client.delete(f'/api/board/{board.id}/')

        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)