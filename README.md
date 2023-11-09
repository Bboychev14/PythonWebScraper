# s05-finalproject-group4
Book Scraper
Book Scraper is a Python tool for scraping book information from Books to Scrape. It provides various options for filtering and manipulating the scraped data.

Table of Contents
Introduction
Features
Installation
Usage
Technical details for GSheets
Testing
Contributing
Introduction
Book Scraper is a command-line tool that allows you to scrape book data from the provided website. You can specify the number of books to scrape, filter books by various criteria, search for books by title, and more. For detailed information on how to use Book Scraper, please refer to the Usage section.

Features
Scrape book data from Books to Scrape.
Filter books by availability, rating, and price.
Sort books by availability, rating, price, title ascending or descending.
Search for books by title.
Extract book information into Google Sheets.
Save scraped data to a JSON file.
Installation
To use Book Scraper, follow these steps:

Clone this repository to your local machine.
This part uses virtualenv with python3. Install the required dependencies by running the following command:
pip install -r requirements.txt
Configure your Google Sheets API credentials. Replace the GOOGLE_SHEETS_KEY environment variable with the path to your credentials JSON file. For detailed information on how to set up the Google Sheets, please refer to the Technical details for GSheets section.
Usage
Valid inputs must include at least one of the following:

b - number of books
g - list of search genres
s - list ordered {ascending, descending}
f - list of filters
d - list of keywords to search for in the description
t - book title search (only one)
w - list of desired book titles to search (from a given title list JSON file)
Book Scraper provides several command-line options to customize your scraping experience. Here are some examples:

python main.py -b 50 -g Science -s rating ascending
python main.py -b 24 -g Classics -f "rating < 3"
python main.py -b 60 -g Science -f "available =14, rating < 3" -d "book"
python main.py -g Science -t "Book Title"
python main.py -w wanted_books.json
For more detailed information on available options and usage, run:

python main.py -h
Technical details for GSheets
Book Scraper includes functionality to export scraped book data to Google Sheets. To set up and use this feature, follow these technical details:

Google Sheets API Credentials
You need to have a Google Cloud project and enable the Google Sheets API for it. Follow the Google Sheets API Quickstart Guide to create a project and enable the API.
Once you've enabled the Google Sheets API, you need to create credentials. Go to the Google Cloud Console, select your project, and navigate to "APIs & Services" > "Credentials."
Click on "Create credentials" and select "Service Account Key." Follow the prompts to create a service account key, choose the "Editor" role, and generate a JSON key file. Save this JSON key file securely.
Rename the JSON key file to something meaningful, e.g., gsheets-credentials.json, and keep it in a secure location. Do not share this file or commit it to version control.
Set the environment variable GOOGLE_SHEETS_KEY to the path of the JSON key file you generated. You can do this in your shell or by editing your project's environment variables.
Usage
Once you've configured the Google Sheets API credentials, you can use the Google Sheets export functionality as follows:

After scraping book data using Book Scraper, you can export the data to a Google Sheets worksheet using the GoogleSheetsHandler.write_to_worksheet(scraped_books) method.
The data will be written to the Google Sheets worksheet specified in the SAMPLE_SPREADSHEET_ID variable within the GoogleSheetsHandler class.
The data will overwrite any existing data in the specified worksheet. Be cautious when using this functionality to avoid data loss.
Make sure that the Google Sheets API is enabled, the credentials file is correctly set in the GOOGLE_SHEETS_KEY environment variable, and your service account has the necessary permissions to write to the specified worksheet.
You can customize the worksheet range and values as needed by modifying the target_range and body parameters when calling the sheet.values().update method within the write_to_worksheet function. That's it! You can now easily export scraped book data to Google Sheets using Book Scraper.
Testing
Book Scraper includes a suite of unit tests to ensure the correctness of its components. To run the tests, use the following command:

python -m unittest test_book_scraper.py
This command will execute the test cases for the BookScraper class, ArgumentParser class, and related functionality.

Contributing
If you'd like to contribute to Book Scraper, please follow these guidelines:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and submit a pull request.
Ensure your code is well-documented and follows PEP 8 coding standards.