from requests_html import HTMLSession
from pprint import pprint
from bs4 import BeautifulSoup
import requests
import shutil
import os
from selenium import webdriver

chrome_driver_path = "/Users/curlos/Desktop/Development/chromedriver"


def get_all_cards_selenium(url):
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        options=options, executable_path=chrome_driver_path)
    driver.get("https://2kdb.net/players")
    popup_okay_button = driver.find_element_by_id('rcc-confirm-button')
    page_buttons = driver.find_elements_by_css_selector(
        'button.p-paginator-page.p-paginator-element.p-link')
    popup_okay_button.click()

    for page_num in range(len(page_buttons)):
        page_buttons[page_num].click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        card_img_link_elems = soup.select('td a')

        for elem in card_img_link_elems:
            print(elem['href'])
            # card_img_link = elem['href']
            # card_url = f"https://2kdb.net{card_img_link}"
            # get_one_card(card_url)

    driver.quit()


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
get_all_cards_selenium('https://2kdb.net/players')
print('ab')
