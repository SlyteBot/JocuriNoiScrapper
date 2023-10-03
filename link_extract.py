import requests
from bs4 import BeautifulSoup
from game import Game
from os.path import exists
from extract import get_response_page

# product-image-container


def download_image(url: str):
    # TODO download image given a link
    pass


def get_games(urls: [str]):
    # TODO get all info from games
    pass


def get_alinks(response: requests.Response):
    text = response.text
    soup = BeautifulSoup(text, 'html.parser')

    data_link = soup.find_all('a', class_='primary')
    data_image = soup.find_all('img', class_='preview img-responsive')
    print(data_link[0]['href'])
    print(data_image[0]['src'])


if __name__ == '__main__':
    url = "https://www.jocurinoi.ro/ps5"
    response = get_response_page(url)
    get_alinks(response)
