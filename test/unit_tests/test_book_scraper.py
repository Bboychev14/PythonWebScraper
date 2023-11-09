import unittest
from argparse import Namespace
from io import StringIO
from unittest import mock
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from module.modules.book import Book
from module.modules.book_scraper import BookScraper


class TestBookScraper(unittest.TestCase):

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_scrape_books(self, mock_create_document_parser_for_url):
        arguments = Namespace(books_count=1, description=[], filtering_params=[], genres=['Travel', 'Mystery'],
                              sorting_params=[], title=[], wanted=[])
        scraper = BookScraper(arguments)

        mock_parser = Mock()
        mock_create_document_parser_for_url.return_value = mock_parser

        scraper._BookScraper__scrape_books_info = Mock()
        scraper._BookScraper__scrape_books_info.return_value = [
            Book("Title1", "Genre1", "10.99", 4, "In Stock", "Description1"),
            Book("Title2", "Genre2", "9.99", 3, "In Stock", "Description2")
        ]

        scraper._BookScraper__sort_books = Mock()

        result = scraper.scrape_books()
        self.assertEqual(len(result), 0)

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_books_info(self, mock_stdout):
        books = [
            Book("Title1", "Genre1", "10.99", 4, "In Stock", "Description1"),
            Book("Title2", "Genre2", "9.99", 3, "In Stock", "Description2")
        ]

        expected_output = (
            "Book 1:\n"
            "Title: Title1\n"
            "Genre: Genre1\n"
            "Price: 10.99\n"
            "Rating: 4\n"
            "Availability: In Stock\n"
            "Description: Description1\n"
            "\n"
            "Book 2:\n"
            "Title: Title2\n"
            "Genre: Genre2\n"
            "Price: 9.99\n"
            "Rating: 3\n"
            "Availability: In Stock\n"
            "Description: Description2\n"
            "\n"
        )

        BookScraper.print_books_info(books)
        actual_output = mock_stdout.getvalue()

        self.assertEqual(actual_output, expected_output)

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_extract_genres_urls_from_page__returns_wanted_genres_list(self, mock_create_dock_parser):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=['Travel', 'Mystery'],
                                   sorting_params=[], title=[], wanted=[])

        with open('test_html.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_dock_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        expected_urls = [
            'http://books.toscrape.com/catalogue/category/books/travel_2/',
            'http://books.toscrape.com/catalogue/category/books/mystery_3/']
        self.assertEqual(expected_urls, scraper.urls_to_scrape_from)

    def test_init_titles_to_search_for_in_book_scraper__passed_t_flag__fill_titles_to_search_for_with_one_title(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=['Test title'], wanted=[])
        scraper = BookScraper(test_arguments)
        self.assertEqual(['Test title'], scraper.titles_to_search_for)

    def test_init_books_count_to_search_for__passed_t_flag__makes_books_count_equal_to_1(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=['Test title'], wanted=[])
        scraper = BookScraper(test_arguments)
        self.assertEqual(1, scraper.books_to_extract_count)

    @patch('module.modules.book_scraper.JSONHandler.extract_titles_from_json')
    def test_init_titles_to_search_for_book_scraper__passed_w_flag_two_titles__fill_titles_to_search_for_with_2_titles(
            self, mock_json_handler):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=['wanted.json'])
        mock_json_handler.return_value = ['Test title one', 'Test title two']
        scraper = BookScraper(test_arguments)
        self.assertEqual(['Test title one', 'Test title two'], scraper.titles_to_search_for)

    @patch('module.modules.book_scraper.JSONHandler.extract_titles_from_json')
    def test_init_books_count__passed_w_flag__makes_books_count__equal_to_passed_book_titles(self, mock_json_handler):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=['wanted.json'])
        mock_json_handler.return_value = ['Test title one', 'Test title two']
        scraper = BookScraper(test_arguments)
        self.assertEqual(2, scraper.books_to_extract_count)

    def test_init_books_to_extract_count__not_passed_b_flag__books_to_extract_count_is_minus_one(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        scraper = BookScraper(test_arguments)
        self.assertEqual(-1, scraper.books_to_extract_count)

    def test_init_books_to_extract_count__passed_b_flag__books_to_extract_count_equal_to_passed_number(self):
        test_arguments = Namespace(books_count=5, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        scraper = BookScraper(test_arguments)
        self.assertEqual(5, scraper.books_to_extract_count)

    def test_init_filtering_params__when_passed_f_flag__filtering_params_is_list_with_dict(self):
        filtering_dict = {'filter_choice': 'price',
                          'filter_operator': '>',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        scraper = BookScraper(test_arguments)
        self.assertEqual([filtering_dict], scraper.filtering_params)

    def test_init_sorting_params__when_passed_s_flag__sorting_params_is_dict_with_tuple(self):
        sorting_params = ('price', 'ascending')
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[sorting_params], title=[], wanted=[])
        scraper = BookScraper(test_arguments)
        self.assertEqual([sorting_params], scraper.sorting_params)

    def test_init_urls_to_scrape_from__when_no_g_flag_passed__contains_all_genres_url(self):
        expected_url = 'http://books.toscrape.com/catalogue/category/books_1/'
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        self.assertEqual(expected_url, scraper.urls_to_scrape_from[0])

    def test_init_titles_to_search_for__no_t_or_w_flag_passed__titles_to_search_for_is_empty_list(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        self.assertEqual([], scraper.titles_to_search_for)

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scrape_book_info__passed_1_books__return_list_with_1_books(self, mock_doc_parser):
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)

        mock_doc_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('A Light in the Attic', 'Poetry', '£51.77', 3, 22,
                                                                    'testDescr')
        scraper.scrape_books()

        book1 = Book('A Light in the Attic', 'Poetry', '£51.77', 3, 22, 'testDescr')

        expected = [book1]
        self.assertEqual(len(expected), len(scraper.books_info))
        self.assertEqual(expected[0].title, scraper.books_info[0].title)

    def test_book_scraper__sort_extracted_books_by_price_ascending(self):
        test_arguments = Namespace(books_count=2, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('price', 'ascending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('A Light in the Attic', 'Poetry', '£2', 3, 22, 'testDescr')
        book2 = Book('A Light in the Attic', 'Poetry', '£1', 3, 22, 'testDescr')
        book3 = Book('A Light in the Attic', 'Poetry', '£3', 3, 22, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book2.price, scraper.books_info[0].price)

    def test_book_scraper__sort_extracted_books_by_price_descending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('price', 'descending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('A Light in the Attic', 'Poetry', '£2', 3, 22, 'testDescr')
        book2 = Book('A Light in the Attic', 'Poetry', '£1', 3, 22, 'testDescr')
        book3 = Book('A Light in the Attic', 'Poetry', '£3', 3, 22, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book3.price, scraper.books_info[0].price)
        self.assertEqual(book2.price, scraper.books_info[2].price)

    def test_book_scraper__sort_extracted_books_by_title_ascending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('title', 'ascending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 3, 22, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 3, 22, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 3, 22, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book2.title, scraper.books_info[0].title)
        self.assertEqual(book3.price, scraper.books_info[2].price)

    def test_book_scraper__sort_extracted_books_by_title_descending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('title', 'descending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 3, 22, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 3, 22, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 3, 22, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book3.title, scraper.books_info[0].title)
        self.assertEqual(book2.price, scraper.books_info[2].price)

    def test_book_scraper__sort_extracted_books_by_availability_ascending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('availability', 'ascending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 3, 1, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 3, 3, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book2.availability, scraper.books_info[0].availability)
        self.assertEqual(book3.availability, scraper.books_info[2].availability)

    def test_book_scraper__sort_extracted_books_by_availability_descending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('availability', 'descending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 3, 1, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 3, 3, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book3.availability, scraper.books_info[0].availability)
        self.assertEqual(book2.availability, scraper.books_info[2].availability)

    def test_book_scraper__sort_extracted_books_by_rating_ascending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('rating', 'ascending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 1, 1, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 2, 3, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book2.rating, scraper.books_info[0].rating)
        self.assertEqual(book1.rating, scraper.books_info[2].rating)

    def test_book_scraper__sort_extracted_books_by_rating_descending(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('rating', 'descending')], title=[], wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 1, 1, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 2, 3, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book1.rating, scraper.books_info[0].rating)
        self.assertEqual(book2.rating, scraper.books_info[2].rating)

    def test_book_scraper__sort_books_by_second_sort_param_if_first_is_equal(self):
        test_arguments = Namespace(books_count=-1, description=[], filtering_params=[], genres=[],
                                   sorting_params=[('rating', 'descending'), ('price', 'ascending')], title=[],
                                   wanted=[])

        scraper = BookScraper(test_arguments)
        scraper._BookScraper__scrape_books_info = mock.Mock()
        book1 = Book('B', 'Poetry', '£2', 1, 2, 'testDescr')
        book2 = Book('A', 'Poetry', '£1', 1, 1, 'testDescr')
        book3 = Book('C', 'Poetry', '£3', 2, 3, 'testDescr')
        scraper.books_info = [book1, book2, book3]
        scraper._BookScraper__scrape_books_info.return_value = None
        scraper.scrape_books()
        self.assertEqual(book3.price, scraper.books_info[0].price)
        self.assertEqual(book1.price, scraper.books_info[2].price)
        self.assertEqual(book2.price, scraper.books_info[1].price)

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scraper_filter_books_by_price__when_filter_is_not_met__returns_empty_list(self,
                                                                                            mock_create_parser):
        filtering_dict = {'filter_choice': 'price',
                          'filter_operator': '>',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html_for_filtering_books.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('B', 'Poetry', '£2', 1, 2, 'testDescr')
        scraper.scrape_books()
        self.assertEqual([], scraper.books_info)

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scraper_filter_books_by_price__when_filter_is_met__returns_list_one_element(self,
                                                                                              mock_create_parser):
        filtering_dict = {'filter_choice': 'price',
                          'filter_operator': '=',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html_for_filtering_books.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('B', 'Poetry', '£2', 1, 2, 'testDescr')
        scraper.scrape_books()
        self.assertEqual(1, len(scraper.books_info))

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scraper_filter_books_by_rating__when_filter_is_not_met__returns_empty_list(self, mock_create_parser):
        filtering_dict = {'filter_choice': 'rating',
                          'filter_operator': '>',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html_for_filtering_books.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('B', 'Poetry', '£2', 1, 2, 'testDescr')
        scraper.scrape_books()
        self.assertEqual(0, len(scraper.books_info))

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scraper_filter_books_by_rating__when_filter_is_met__returns_list_one_element(self,
                                                                                               mock_create_parser):
        filtering_dict = {'filter_choice': 'rating',
                          'filter_operator': '>',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html_for_filtering_books.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        scraper.scrape_books()
        self.assertEqual(1, len(scraper.books_info))

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scraper_filter_books_by_availability__when_filter_is_not_met__returns_empty_list(self,
                                                                                                   mock_create_parser):
        filtering_dict = {'filter_choice': 'availability',
                          'filter_operator': '>',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html_for_filtering_books.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        scraper.scrape_books()
        self.assertEqual(0, len(scraper.books_info))

    @patch('module.modules.book_scraper.create_document_parser_for_url')
    def test_book_scraper_filter_books_by_availability__when_filter_is_met__returns_list_one_el(self,
                                                                                                mock_create_parser):
        filtering_dict = {'filter_choice': 'availability',
                          'filter_operator': '=',
                          'filter_value': 2,
                          }
        test_arguments = Namespace(books_count=1, description=[], filtering_params=[filtering_dict], genres=[],
                                   sorting_params=[], title=[], wanted=[])
        with open('test_html_for_filtering_books.html', 'r', encoding='UTF-8') as file:
            create_parser_return_value = BeautifulSoup(file)
        mock_create_parser.return_value = create_parser_return_value
        scraper = BookScraper(test_arguments)
        scraper._BookScraper__extract_book_info = mock.Mock()
        scraper._BookScraper__extract_book_info.return_value = Book('B', 'Poetry', '£2', 3, 2, 'testDescr')
        scraper.scrape_books()
        self.assertEqual(1, len(scraper.books_info))


if __name__ == '__main__':
    unittest.main()