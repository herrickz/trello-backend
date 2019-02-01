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
    order = models.IntegerField(default=0, null=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return f'name: {self.name}, order: {self.order}'

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_card = Card.objects.filter(trelloList__id=self.trelloList.id).order_by('-order').first()

            if last_card is not None:
                self.order = last_card.order + 1
            else:
                self.order = 0

        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('trelloList', 'order',)
