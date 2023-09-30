import requests
from bs4 import BeautifulSoup
from game import Game
from os.path import exists
def get_response_page(url,save = False):
    response = requests.get(url)
    if response.ok == True:
        if save == True:
            with open("test.html","w",encoding="utf-8") as f:
                f.write(response.text)
        return response
    else:
        return None
    

def get_game_name_platform(text: str):
    name, platform = "",""

    first_part,second_part = "Joc", "pentru"
    first_index,last_index = text.find("Joc"),text.find("pentru")
    
    name_start, name_end = first_index + len(first_part), last_index
    platform_start, platform_end = last_index + len(second_part),len(text)
    
    name = text[name_start:name_end].strip()
    platform = text[platform_start:platform_end].strip()
    
    return name,platform

def get_price(soup: BeautifulSoup):
    text = soup.find('div',class_="pret").text
    price_index = text.find('lei')
    price = text[:price_index]
    return price

def get_other_relative_info(soup: BeautifulSoup):
    #TODO Doesn't work on every case need to check if I have the right row
    text = soup.find('table',class_= "table table-striped")
    list_data = text.find_all('td',class_='')
    publisher = list_data[1].text.strip()
    developer = list_data[2].text
    genres = [text.strip() for text in list_data[4].text.split('\n')]
    age = list_data[3].text
    date = list_data[5].text
    return publisher,developer,genres,age,date

def get_info_from_response(response: requests.Response, test = True):
    
    text = response.text
    soup = BeautifulSoup(text,'html.parser')
    name,platform = get_game_name_platform(soup.title.text)
    price = get_price(soup)
    publisher,developer,genres,age,date = get_other_relative_info(soup)
    print(name,platform,price,publisher,developer,genres,age,date)
    #TODO put relevant info in a class and upload it to SQL




if __name__ == '__main__':
    url = "https://www.jocurinoi.ro/grand-theft-auto-v-xbox-360"
    response = None
    test = True
    save = False
    if exists('test.html') == False or  test == True:
        response = get_response_page(url,save)
        print("Response generated!")
    get_info_from_response(response,test)