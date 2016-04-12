from django.db import models


class Book(models.Model):
    book_name = models.CharField(max_length=20)

    def __str__(self):
        return self.book_name


class Chapter(models.Model):
    book = models.ForeignKey(Book, blank=True)
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    vocabs = models.TextField()

    def __str__(self):
        return "{}, {}: {}".format(self.book, self.number, self.name)

class VocabListSubmitted(models.Model):
    book = models.CharField(max_length=20)
    number = models.IntegerField()
    name = models.CharField(max_length=50)
    vocabs = models.TextField()
    passcode = models.CharField(max_length=16)

    def __str__(self):
        return "{}, {}: {}".format(self.book, self.number, self.name)
