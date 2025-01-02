import googleapiclient as google
from googleapiclient.discovery import build

books_service = build('books', 'v1', developerKey='AIzaSyDXhIdwT93SDGDd6LyGAYI73UHtPmOacNM')

def get_book(search:str, max:int = 40):
    response = books_service.volumes().list(q = search, maxResults = max).execute()
    return response
