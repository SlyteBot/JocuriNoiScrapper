import requests
from bs4 import BeautifulSoup
from pathlib import Path
from extract import Extractor
import time
import random


class Page:
    def __init__(self, link: str, cover_dir_name: str = None, thumbnail_dir_name: str = None, filename_proxies="proxies.txt") -> None:
        self.link = link
        if cover_dir_name == None:
            self.cover_dir_name = "covers/"
        else:
            self.cover_dir_name = cover_dir_name
        if thumbnail_dir_name == None:
            self.thumbnail_dir_name = "thumbnails/"
        else:
            self.thumbnail_dir_name = cover_dir_name
        Path(self.thumbnail_dir_name).mkdir(parents=False, exist_ok=True)
        Path(self.cover_dir_name).mkdir(parents=False, exist_ok=True)
        self.proxies = []

        with open(filename_proxies, mode="r") as f:
            for proxy in f:
                self.proxies.append(proxy.strip())
        self.index_proxy = random.randint(0, len(self.proxies)-1)

    def get_proxy(self):
        if self.index_proxy >= len(self.proxies):
            self.index_proxy = 0
        proxies = {
            'https': self.proxies[self.index_proxy]}
        self.index_proxy += 1
        return proxies

    def get_response_page(self, url):
        try:
            response = requests.get(url, proxies=self.get_proxy())

            # if save == True:
            #    with open("test.html", "w", encoding="utf-8") as f:
            #        f.write(response.text)
            return response

        except requests.RequestException as e:
            print(f"Couldn't get response from {self.link}")
            return None

    def download_thumbnail(self, link: str, img_name: str):
        with open(f'{self.thumbnail_dir_name}/{img_name}.webp', 'wb') as f:
            try:
                f.write(requests.get(link).content)
            except requests.exceptions.HTTPError:
                print(f'Couldn\'t get thumbnail for {img_name}')

    def start_extract(self, link: str, thumbnail_link: str, id_name: str):
        response = self.get_response_page(link)
        if response == None:
            return None
        instance_extract = Extractor(response=response, id_name=id_name, thumbnail_link=thumbnail_link,
                                     cover_dir_name=self.cover_dir_name, thumbnail_dir_name=self.thumbnail_dir_name)
        return instance_extract.get_info_from_response()

    def get_all_games(self):
        games = []
        response = self.get_response_page(self.link)
        if response == None:
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', class_="primary")
        product_links = []
        image_links = []
        img_name = []
        for tag in links:
            product_links.append(tag['href'])
            img_name.append(tag['href'].rsplit('/', 1)[-1])
            image_links.append(tag.find('img')['src'])
        for page_link, thumbnail_link, id_name in zip(product_links, image_links, img_name):
            print(f"Extracting for {id_name}")
            result = self.start_extract(page_link, thumbnail_link, id_name)
            time.sleep(random.randint(25, 35))
            print(f"Done for {id_name}")
            if result is not None:
                games.append(result)
        return games


if __name__ == "__main__":
    link = "https://www.jocurinoi.ro/xbox-series&page=1"
    instance = Page(link)

    print(instance.get_all_games())
