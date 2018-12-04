from django.db import models
import hashlib, time

def _createHash():
    hash = hashlib.sha1()
    hash.update(str(time.time()).encode('utf-8'))

    return hash.hexdigest()[:10]

class Board(models.Model):
    name = models.TextField()
    hashId = models.CharField(max_length=10, default=_createHash, unique=True, editable=False)

    def __str__(self):
        return f'name: {self.name}, hashId: {self.hashId}'

class List(models.Model):
    name = models.TextField()
    board = models.ForeignKey(Board, related_name='lists', on_delete=models.CASCADE)

    def __str__(self):
        return f'name: {self.name}, board: {{ {self.board} }}'

class Card(models.Model):
    name = models.TextField()
    trelloList = models.ForeignKey(List, related_name='cards', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
