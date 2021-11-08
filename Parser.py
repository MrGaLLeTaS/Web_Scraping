from bs4 import BeautifulSoup
import cloudscraper
import datetime
import csv
import json
import time

URL = 'https://yummyanime.club/anime-updates'

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.61',
    'accept': '*/*'
}

start_time = time.time()


def get_html(url):
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': False
        }
    )
    r = scraper.get(url)
    return r


def get_data(html):
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    with open(f"yummyanime_{cur_time}.csv", "w", encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Название аниме",
                "Обновление",
                "Ссылка"
            )
        )

    soup = BeautifulSoup(html, 'lxml')
    HOST = 'https://yummyanime.club'
    anime = soup.find('ul', class_='update-list date-list').find_all('li')
    animes_data = []
    for anm in anime:
        anime_data = anm.find_all('a')
        try:
            title = anime_data[0].find('span', class_='update-title').get_text(strip=True)
        except:
            title = 'Название не найдено'
        try:
            update = anime_data[0].find('span', class_='update-info').get_text(strip=True)
        except:
            update = 'Обновление не найдено'
        try:
            link = anime_data[-1].get('href')
        except:
            link = 'Ссылка не найдена'

        animes_data.append({
            'title': title,
            'update': update,
            'link': HOST + link
        })

        with open(f"yummyanime_{cur_time}.csv", 'a', newline='', encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    title,
                    update,
                    HOST + link
                )
            )

        with open(f"yummyanime_{cur_time}.json", 'w', encoding="utf-8") as file:
            json.dump(animes_data, file, indent=3, ensure_ascii=False)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_data(html.text)
    else:
        print("Error 403")
    finish_time = time.time() - start_time
    print(finish_time)


if __name__ == '__main__':
    parse()
