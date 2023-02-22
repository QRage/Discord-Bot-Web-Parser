import requests
from bs4 import BeautifulSoup


forum_domain = 'http://www.pathofexile.com'

thread_en = "https://www.pathofexile.com/forum/view-thread/3290069/page/1"
thread_ru = "https://www.pathofexile.com/forum/view-thread/2551118/page/1"
headers = {
    "Authorization": "SAPISIDHASH 1623130218_185509d60d328a8b7be39f8419e3d33422df715c",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
}


def parse_page(url, header):
    request = requests.get(url, headers=header)
    page_source = request.text

    soup = BeautifulSoup(page_source, "lxml")

    return soup


def get_last_page_href(url):
    soup = parse_page(url, headers)

    forum_page_path = soup.select_one('.topBar a:nth-of-type(6)').get('href')
    forum_page_link = forum_domain + forum_page_path

    return forum_page_link


def get_all_posts_from_page(url):
    soup = parse_page(url, headers)

    table = soup.find(lambda tag: tag.name == 'table')
    rows = table.findAll(lambda tag: tag.name == 'tr')

    posts = [{
        'username': f'{post.findAll("a")[1].text}',
        'profile_url': f'{forum_domain + post.findAll("a")[1].get("href")}',
        'message': f'{post.find("div", class_="content").text}'

    } for post in rows]

    return posts


def get_last_post(forum_thread_link):
    return get_all_posts_from_page(get_last_page_href(forum_thread_link))[-1]


if __name__ == '__main__':
    print(get_last_post(thread_en))
    print(get_last_post(thread_ru))
