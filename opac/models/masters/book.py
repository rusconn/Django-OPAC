from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from django.db.models import Q

from opac.models.abstracts import TimeStampedModel
from opac.models.masters.publisher import Publisher


class Book(TimeStampedModel):
    class Meta:
        verbose_name = '書籍'
        verbose_name_plural = '書籍'

    name = models.CharField(
        '書名',
        max_length=100
    )
    publisher = models.ForeignKey(
        Publisher,
        verbose_name='出版者',
        related_name='books',
        on_delete=models.PROTECT
    )
    publication_date = models.DateField(
        '出版日',
        blank=True,
        null=True
    )
    size = models.CharField(
        '大きさ',
        max_length=20,
        blank=True,
        null=True
    )
    page = models.IntegerField(
        'ページ数',
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )
    isbn = models.CharField(
        'ISBN',
        max_length=13,
        blank=True,
        null=True,
        validators=[
            # ISBN10 or ISBN13 without separators
            RegexValidator(regex=r'^(97(8|9))?\d{9}(\d|X)$')
        ]
    )

    def __str__(self):
        return self.name

    def author_names(self):
        return (a.name for a in self.authors.all())

    def translator_names(self):
        return (t.name for t in self.translators.all())

    @staticmethod
    def search(words):
        queryset = Book.objects.none()
        for word in words:
            books = Book.objects \
                .filter(
                    Q(name__icontains=word) |
                    Q(authors__name__icontains=word) |
                    Q(translators__name__icontains=word) |
                    Q(publisher__name__icontains=word)) \
                .distinct()
            queryset = queryset.union(books)
        return queryset.order_by('id')
