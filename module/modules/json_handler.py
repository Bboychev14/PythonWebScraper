import json
import sys

class JSONHandler:
    """
    Helper class to take care of all operations connected to JSON.
    No state, only statick methods.
    """

    @staticmethod
    def save_books_to_json(books, file_name='data.json'):
        """
        Saving the scraped books in json file.
        :param books: The book's objects to be saved in json fail
        :param file_name: The name of the file that we will be creating
        """

        book_list = []
        for book in books:
            book_dict = {
                'title': book.title,
                'genre': book.genre,
                'price': book.price,
                'rating': book.rating,
                'availability': book.availability,
                'description': book.description
            }
            book_list.append(book_dict)

        with open(file_name, 'w', encoding='UTF-8') as json_file:
            json.dump(book_list, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def extract_titles_from_json(file_name):
        """
        Taking book's titles from passed json file and assigning it to titles_to_search_for
        :param file_name: The name of the file passed by the user.
        :return: None
        """
        try:
            with open(file_name, 'r') as file:
                data = json.load(file)
            book_titles = data.get('book_titles', [])
            book_titles = set(book_titles)
            return book_titles
        except FileNotFoundError:
            print(f"File {file_name} is not found!")

