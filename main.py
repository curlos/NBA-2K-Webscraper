from pprint import pprint
from bs4 import BeautifulSoup
import requests
import shutil
import os


def get_all_cards(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')


def get_one_card(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    card_img = soup.select('.image img')[0]
    card_img_link = card_img['src']
    filename = card_img_link.split('/players/')[1]
    save_dir = '2K Cards'

    print('--------')
    pprint(card_img)
    pprint(card_img_link)
    print(filename)

    print(f"Downloading {filename}...")

    r = requests.get(card_img_link, stream=True)

    if r.status_code == 200:
        r.raw.decode_content = True

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        shutil.move(filename, save_dir)
        print(f"{filename} downloaded successfully")
    else:
        print(f"{filename} failed to download")


# get_one_card('https://2kdb.net/player/2k20/michael-jordan/9152')

print('ab')
