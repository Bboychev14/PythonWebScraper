class Book:
    """
    Class for storing data about each book.
    """

    RATING_CONVERTER_MAPPER = {
        'One': 1,
        'Two': 2,
        'Three': 3,
        'Four': 4,
        'Five': 5,
    }

    def __init__(self, title, genre, price, rating, availability, description):
        self.title = title
        self.genre = genre
        self.price = price
        self.rating = rating
        self.availability = availability
        self.description = description

    def __str__(self):
        return f"Title: {self.title}\n" \
               f"Genre: {self.genre}\n" \
               f"Price: {self.price}\n" \
               f"Rating: {self.rating}\n" \
               f"Availability: {self.availability}\n"\
               f"Description: {self.description}"
