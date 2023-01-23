from django.db import models


# Create your models here.


class Phrase(models.Model):
    CATEGORY = (
        ('Technical Article', 'Technical Article'),
        ('Documentation', 'Documentation'),
        ('Proposals', 'Proposals'),
        ('White Papers', 'White Papers'),
        ('Instruction Manuals', 'Instruction Manuals'),
        ('Essay', 'Essay'),
        ('Medical Technical Writing', 'Medical Technical Writing')
    )
    word = models.CharField(max_length=100)
    category = models.CharField(max_length=150, default="Technical Article", choices=CATEGORY)

    def __str__(self):
        return f"word - {self.word}: {self.category}"

    class Meta:
        ordering = ('-id',)


class ArticleTopic(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, related_name='topics')
    title = models.TextField(max_length=150)

    def __str__(self):
        return self.phrase.word + ': ' + self.title

    class Meta:
        ordering = ('-id',)


class Counter(models.Model):
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.count)

    class Meta:
        ordering = ('-id',)
