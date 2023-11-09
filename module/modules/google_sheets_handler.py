from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd
import os


class GoogleSheetsHandler:
    """
    Helper class for parsing and exporting Book objects to Google Sheets.
    """
    google_sheets_key = os.environ.get('GOOGLE_SHEETS_KEY')
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SAMPLE_SPREADSHEET_ID = '1hyzltTl6U8wLp4q93NWqpROLF9UR0VYerLWnmQUt8Vk'

    @staticmethod
    def write_to_worksheet(scraped_books):
        """
        Writes information about each book in the worksheet.
        :param scraped_books: list of book objects.
        """
        if not scraped_books:
            return
        creds = service_account.Credentials.from_service_account_file(
            GoogleSheetsHandler.google_sheets_key, scopes=GoogleSheetsHandler.SCOPES)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Clears the old information in the sheet.
        sheet.values().clear(spreadsheetId=GoogleSheetsHandler.SAMPLE_SPREADSHEET_ID, range="data").execute()

        books_data_frame = pd.DataFrame([vars(book) for book in scraped_books])
        books_data_frame_list = books_data_frame.values.tolist()
        headers = [header.capitalize() for header in books_data_frame.columns.values.tolist()]

        target_range = "data!A1"  # Defines the target range where the data will be written in the spreadsheet.
        sheet.values().update(spreadsheetId=GoogleSheetsHandler.SAMPLE_SPREADSHEET_ID,
                              range=target_range, valueInputOption="USER_ENTERED",
                              body={"values": [headers] + books_data_frame_list}).execute()
