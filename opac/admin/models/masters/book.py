from django.contrib import admin

from opac.models.masters.book import Book


class BookAdmin(admin.ModelAdmin):
    class AuthorsInline(admin.TabularInline):
        model = Book.authors.through
        verbose_name = '著者'
        raw_id_fields = ('author', )
        extra = 1

    class TranslatorsInline(admin.TabularInline):
        model = Book.translators.through
        verbose_name = '訳者'
        raw_id_fields = ('translator', )
        extra = 1

    list_display = (
        'get_book_number',
        'name',
        'get_authors',
        'get_translators',
        'get_publisher_name',
        'issue_date',
        'size',
        'page',
        'isbn'
    )
    list_display_links = ('get_book_number', 'name')
    search_fields = ('name', 'publisher__name', 'isbn')
    raw_id_fields = ('publisher', )
    inlines = (AuthorsInline, TranslatorsInline)

    def get_queryset(self, request):
        return (
            Book.objects
                .select_related('publisher')
                .prefetch_related('authors')
                .prefetch_related('translators')
        )

    def get_book_number(self, book):
        return book.id
    get_book_number.admin_order_field = 'id'
    get_book_number.short_description = ' 書籍番号'

    def get_authors(self, book):
        return ', '.join(a.name for a in book.authors.all()) \
            or None
    get_authors.short_description = '著者'

    def get_translators(self, book):
        return ', '.join(t.name for t in book.translators.all()) \
            or None
    get_translators.short_description = '訳者'

    def get_publisher_name(self, book):
        return book.publisher.name
    get_publisher_name.admin_order_field = 'publisher__name'
    get_publisher_name.short_description = '出版者'


admin.site.register(Book, BookAdmin)
