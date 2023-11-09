from module.modules.book import Book
from module.modules.common import create_document_parser_for_url
from module.modules.json_handler import JSONHandler
from operator import attrgetter


class BookScraper:
    """
    Main class for making requests to the server, scraping and parsing data.
    """

    WORKING_URL = 'http://books.toscrape.com/'
    ALL_GENRES_URL = 'http://books.toscrape.com/catalogue/category/books_1/'

    def __init__(self, arguments):

        self.books_to_extract_count = arguments.books_count
        self.filtering_params = arguments.filtering_params
        self.keywords_to_search_for = arguments.description
        self.sorting_params = arguments.sorting_params
        self.titles_to_search_for = []
        self.urls_to_scrape_from = [BookScraper.ALL_GENRES_URL]

        self.books_info = []

        self.__init_attributes(arguments)

        self.filter_options_mapper = {
            'availability': lambda book: book.availability,
            'rating': lambda book: book.rating,
            'price': lambda book: float(book.price.replace('£', ''))
        }

        self.filter_operators_mapper = {
            '<': lambda filter_by, value_to_compare: filter_by < value_to_compare,
            '>': lambda filter_by, value_to_compare: filter_by > value_to_compare,
            '=': lambda filter_by, value_to_compare: filter_by == value_to_compare,
            '!=': lambda filter_by, value_to_compare: filter_by != value_to_compare,
            '<=': lambda filter_by, value_to_compare: filter_by <= value_to_compare,
            '>=': lambda filter_by, value_to_compare: filter_by >= value_to_compare,
        }

    def scrape_books(self):
        """
        Taking care for extracting books from all the urls that are passed by the user arguments.
        The, if self.books_to_extract_count is for optimization purposes.
        """
        for url in self.urls_to_scrape_from:
            if self.books_to_extract_count == 0:
                break

            self.__scrape_books_info(url)

        self.__sort_books()
        JSONHandler.save_books_to_json(self.books_info)
        return self.books_info

    def __sort_books(self):
        """
        Sorting the result list with books by different criteria and reverse order.
        It starts to loop from the least significant sorting criteria, so that we can keep
        the reverse order.
        """
        for sort_param_index in range(len(self.sorting_params) - 1, -1, -1):
            sort_by, sorting = self.sorting_params[sort_param_index]
            is_reversed = True if sorting == 'descending' else False
            self.books_info.sort(key=attrgetter(sort_by), reverse=is_reversed)

    def __is_book_good_for_scraping(self, book):
        """
        Apply all the different parameters that need to be taken in consideration when scraping book.
        :param book: The book that we are testing
        :return: Boolean
        """

        for cur_filter in self.filtering_params:
            filter_by = self.filter_options_mapper[cur_filter['filter_choice']](book)
            if not self.filter_operators_mapper[cur_filter['filter_operator']](filter_by,
                                                                               int(cur_filter['filter_value'])):
                return False

        for cur_keyword in self.keywords_to_search_for:
            if cur_keyword not in book.description:
                return False

        return True

    def __scrape_books_info(self, url_to_extract_from):
        """
        Taking care for scraping N number of books.

        :param url_to_extract_from: Current starting point url to extract from.
        :return: None
        """

        document_parser = create_document_parser_for_url(url_to_extract_from)

        while True:
            books_article_tags = document_parser.find_all('article', class_='product_pod')

            if self.titles_to_search_for:
                books_article_tags = self.__return_books_by_title(books_article_tags)

            for book in books_article_tags:

                book_detail_page_url = self.__form_book_detail_page_url(book)
                book = self.__extract_book_info(book_detail_page_url)

                if self.__is_book_good_for_scraping(book):
                    self.books_info.append(book)
                    self.books_to_extract_count -= 1

                if self.books_to_extract_count == 0:
                    return None

            try:
                document_parser = self.__return_document_parser_for_next_page(url_to_extract_from, document_parser)
            except AttributeError:
                return None

    def __init_attributes(self, arguments):
        """
        Parsing arguments passed by argument_parser and setting class attrs.
        :param arguments: Arguments passed by the user
        :return: None
        """
        if arguments.genres:
            self.__extract_genres_urls_from_page(arguments.genres)

        if arguments.title or arguments.wanted:
            self.titles_to_search_for = arguments.title or JSONHandler.extract_titles_from_json(arguments.wanted[0])
            self.books_to_extract_count = len(self.titles_to_search_for)

    def __extract_genres_urls_from_page(self, genres):
        """
        Taking the urls of the genres that are passed by the user and parsing them.
        :param genres: List of genres passed by the user.
        Return: None
        """

        document_parser = create_document_parser_for_url(BookScraper.WORKING_URL)

        genres_div_tag = document_parser.find('div', class_='side_categories')
        genres_li_tags = genres_div_tag.select('ul li a')
        self.urls_to_scrape_from.clear()
        for genre in genres_li_tags:
            genre_name = genre.text.strip()
            if genre_name in genres:
                self.urls_to_scrape_from.append(BookScraper.WORKING_URL + genre.get('href').replace('index.html', ''))
            if len(self.urls_to_scrape_from) == len(genres):
                break

    def __return_books_by_title(self, all_books_article_tags):
        """
        If we have -t or -w flag this method is called in order
        to filter the books by their title, without opening the detail page of it.
        :param all_books_article_tags: all book article tags on the current page.
        :return: filtered list of book by title.
        """

        books = [book_article_tag for book_article_tag in all_books_article_tags if
                 book_article_tag.select_one('h3 a').get('title') in self.titles_to_search_for]

        return books

    @staticmethod
    def __extract_book_info(book_url):
        """
        Gathers data for single book.
        :param book_url: The url for the detail page of the book
        :return: Instance of class Book

        """

        document_parser = create_document_parser_for_url(book_url)

        book_title = document_parser.h1.string
        book_genre = document_parser.select('ul.breadcrumb li')[2].select_one('a').text
        book_price = document_parser.select_one('p.price_color').get_text().lstrip("Â")
        book_rating = Book.RATING_CONVERTER_MAPPER[document_parser.select_one('p.star-rating')['class'][1]]
        book_availability_string = document_parser.select_one('p.instock.availability').get_text(strip=True)
        book_availability = int(''.join([el for el in book_availability_string if el.isdigit()]))
        book_description = document_parser.find('div', class_='sub-header').findNextSibling().text

        temp_book = Book(book_title, book_genre, book_price, book_rating, book_availability, book_description)

        return temp_book

    @staticmethod
    def __form_book_detail_page_url(book):
        """
        Depending on where we are on the page(on some genre or not), the book's href,
        may start  with "../../../" or "../../".
        Because of that we are making it bulletproof, so that in the both cases the program will work.
        :param book: The book that we need to form the url for.
        :return: URL for the detail page of the book.
        """
        book_href_url = book.h3.a['href'].replace('../../', '')
        book_href_url = book.h3.a['href'].replace('../', '')
        book_url = BookScraper.WORKING_URL + 'catalogue/' + book_href_url
        return book_url

    @staticmethod
    def print_books_info(books):
        """
        Used for debugging/printing result to the console.
        """
        for i in range(len(books)):
            print(f'Book {i + 1}:')
            print(books[i])
            print()

    @staticmethod
    def __return_document_parser_for_next_page(url, document_parser):
        """
        Check if we have next page button. If so, returns new BS document parser
        for the next page
        :param url: the current url that we are working on
        :param document_parser: document parser for the current url
        :return: if next page returns new document parser, else raises
        """

        pager_tag = document_parser.find('ul', class_='pager')
        next_page_url_href = pager_tag.find('li', class_='next').findNext().get(
            'href')
        next_page_link = url + next_page_url_href
        new_document_parser = create_document_parser_for_url(next_page_link)
        return new_document_parser
