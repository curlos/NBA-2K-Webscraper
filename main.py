from pprint import pprint
from bs4 import BeautifulSoup
import requests
import shutil
import os


def start_download():
    num_of_pages = int(
        input('How many pages of cards do you want to download? (30 per page): '))
    base_url = 'https://2kmtcentral.com/21/players/page/'

    if num_of_pages <= 0:
        print('Program ended.')
        return

    get_all_cards('https://2kmtcentral.com/21/players', 1)
    offset = 31

    for page_num in range(1, num_of_pages):
        url = f"https://2kmtcentral.com/21/players/page/{page_num}"
        get_all_cards(url, offset)
        offset += 30

    print('All cards finished downloading.')


def get_all_cards(url, offset):
    player_card_img_links = []
    player_card_names = []
    save_dir = '2K Cards Numbered'

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    card_img_elems = soup.select('td img')

    for imgElem in card_img_elems:
        if imgElem.has_attr('data-full'):
            card_img_link = imgElem['data-full']
            player_card_img_links.append(card_img_link)

    name_box_links = soup.select('.name .box-link')

    for name_link in name_box_links:
        full_link = name_link['href']
        full_link_arr = full_link.split('/players/')

        for elem in full_link_arr:
            if not elem.startswith('http'):
                number = elem.split('/')[0]
                player_name = elem.split('/')[1]
                filename = f"{player_name}-{number}.png"
                player_card_names.append(filename)

    for i in range(len(player_card_names)):
        filename, img_link = (player_card_names[i], player_card_img_links[i])
        get_one_card(f"{str(i + offset).zfill(3)}.png",
                     img_link, save_dir)


def get_one_card(filename, img_link, save_dir):

    print(f"Downloading {filename}...", end="")

    r = requests.get(img_link, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        shutil.move(filename, save_dir)
        print(f"Success!")
    else:
        print(f"Failed!")


start_download()
