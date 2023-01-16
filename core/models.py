from django.db import models


# Create your models here.
class Phrase(models.Model):
    word = models.CharField(max_length=100)

    def __str__(self):
        return self.word


class ArticleTopic(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.phrase.word + ': ' + self.title


class Counter(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.count)


