import requests
from bs4 import BeautifulSoup
from game import Game
from os.path import exists


# TODO A WHOLE ASS REFACTORING FUCKER

def get_response_page(url, save=False):
    response = requests.get(url)
    if response.ok == True:
        if save == True:
            with open("test.html", "w", encoding="utf-8") as f:
                f.write(response.text)
        return response
    else:
        return None


def get_game_name_platform(text: str):
    name, platform = "", ""

    first_part, second_part = "Joc", "pentru"
    first_index, last_index = text.find("Joc"), text.find("pentru")

    name_start, name_end = first_index + len(first_part), last_index
    platform_start, platform_end = last_index + len(second_part), len(text)

    name = text[name_start:name_end].strip()
    platform = text[platform_start:platform_end].strip()

    return name, platform


def get_price(soup: BeautifulSoup):
    text = soup.find('div', class_="pret").text
    price_index = text.find('lei')
    price = text[:price_index].strip()
    return price


def get_other_relative_info(soup: BeautifulSoup):
    text = soup.find('table', class_="table table-striped")

    list_data = [list(filter(lambda a: a != '', data.text.split('\n')))
                 for data in text.find_all('td')]
    platform_index, publisher_index, developer_index, gen_index, date_index = list_data.index(['Platforma']), list_data.index(
        ['Producator']), list_data.index(['Dezvoltator']), list_data.index(['Genuri']), list_data.index(['Data lansare'])

    publisher = list_data[publisher_index+1][0]
    developer = list_data[developer_index+1][0]
    genres = list_data[gen_index+1]
    date = list_data[date_index+1][0]
    return publisher, developer, genres, date


def download_main_cover(soup: BeautifulSoup):
    image_link = soup.find('img', class_="main-cover")['src']
    name = "TEST"
    with open(f'{name}.webp', 'wb') as f:
        try:
            f.write(requests.get(image_link).content)
        except requests.exceptions.HTTPError:
            print(f'Couldn\'t get image {name}')


def get_info_from_response(response: requests.Response, test=True):

    text = response.text
    soup = BeautifulSoup(text, 'html.parser')
    name, platform = get_game_name_platform(soup.title.text)
    price = get_price(soup)
    publisher, developer, genres, date = get_other_relative_info(soup)
    # TODO Make image downloading threaded
    download_main_cover(soup)
    info = Game(name, date, price, publisher, developer, platform, genres)

    print(info)
    # TODO put relevant info in a class and upload it to SQL


if __name__ == '__main__':
    url = "https://www.jocurinoi.ro/grand-theft-auto-v-xbox-360"
    response = None
    test = True
    save = False
    if exists('test.html') == False or test == True:
        response = get_response_page(url, save)
        print("Response generated!")
    get_info_from_response(response, test)
