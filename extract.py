import requests
from bs4 import BeautifulSoup
from game import Game
from os.path import exists
import threading
from pathlib import Path


class Extractor:
    def __init__(self, response: requests.Response, id_name: str, thumbnail_link: str, cover_dir_name: str, thumbnail_dir_name: str) -> None:
        self.response = response
        self.id_name = id_name
        self.cover_dir_name = cover_dir_name
        self.thumbnail_dir_name = thumbnail_dir_name
        self.thumbnail_link = thumbnail_link

    def get_game_name_platform(self, text: str):
        name = ""

        first_part, second_part = "Joc", "pentru"
        first_index, last_index = text.find("Joc"), text.find("pentru")

        name_start, name_end = first_index + len(first_part), last_index
        platform_start, platform_end = last_index + len(second_part), len(text)

        name = text[name_start:name_end].strip()
        # platform = text[platform_start:platform_end].strip()

        return name

    def get_price(self, soup: BeautifulSoup):
        text = soup.find('div', class_="pret").text
        price_index = text.find('lei')
        price = text[:price_index].strip()
        return price

    def get_other_relative_info(self, soup: BeautifulSoup):
        text = soup.find('table', class_="table table-striped")

        list_data = [list(filter(lambda a: a != '', data.text.split('\n')))
                     for data in text.find_all('td')]
        platform_index, publisher_index, developer_index, gen_index, date_index = list_data.index(['Platforma']), list_data.index(
            ['Producator']), list_data.index(['Dezvoltator']), list_data.index(['Genuri']), list_data.index(['Data lansare'])
        platform = list_data[platform_index+1][0]
        publisher = list_data[publisher_index+1][0]
        developer = list_data[developer_index+1][0]
        genres = list_data[gen_index+1]
        date = list_data[date_index+1][0]
        return platform, publisher, developer, genres, date

    def download_main_cover(self, soup: BeautifulSoup):
        image_link = soup.find('img', class_="main-cover")['src']
        name = str(self.id_name)
        with open(f'{self.cover_dir_name}/{name}.webp', 'wb') as f:
            try:
                f.write(requests.get(image_link).content)
            except requests.exceptions.HTTPError:
                print(f'Couldn\'t get cover for {name}')

    def download_thumbnail(self):
        name = str(self.id_name)
        with open(f'{self.thumbnail_dir_name}/{name}.webp', 'wb') as f:
            try:
                f.write(requests.get(self.thumbnail_link).content)
            except requests.exceptions.HTTPError:
                print(f'Couldn\'t get cover for {name}')

    def get_info_from_response(self):

        text = self.response.text
        soup = BeautifulSoup(text, 'html.parser')
        name = self.get_game_name_platform(soup.title.text)
        price = self.get_price(soup)
        platform, publisher, developer, genres, date = self.get_other_relative_info(
            soup)
        threading.Thread(target=self.download_main_cover,
                         args=[soup]).start()
        threading.Thread(target=self.download_thumbnail, args=[]).start()
        info = Game(self.id_name, name, date, price, publisher,
                    developer, platform, genres)

        return info
