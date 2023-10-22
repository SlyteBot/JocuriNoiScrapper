import requests
from bs4 import BeautifulSoup
from pathlib import Path
from extract import Extractor


class Page:
    def __init__(self, link: str, cover_dir_name: str = None, thumbnail_dir_name: str = None) -> None:
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

    def get_response_page(self, url):
        response = requests.get(url)
        if response.ok == True:
            # if save == True:
            #    with open("test.html", "w", encoding="utf-8") as f:
            #        f.write(response.text)
            return response
        else:
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
            return
        instance_extract = Extractor(response=response, id_name=id_name, thumbnail_link=thumbnail_link,
                                     cover_dir_name=self.cover_dir_name, thumbnail_dir_name=self.thumbnail_dir_name)
        print(instance_extract.get_info_from_response())

    def get_all_links(self):

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
            self.start_extract(page_link, thumbnail_link, id_name)


if __name__ == "__main__":
    link = "https://www.jocurinoi.ro/ps5&page=1"
    instance = Page(link)
    instance.get_all_links()
