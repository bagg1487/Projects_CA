import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin
import time
from fake_useragent import UserAgent

class DromParser:
    BASE_URL = "https://baza.drom.ru"
    DEFAULT_REGION = "novosibirskaya-obl"

    def __init__(self, region: str = None, delay: float = 1.0):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.delay = delay
        self.region = region or self.DEFAULT_REGION

    def _get(self, url, params=None):
        headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        }
        time.sleep(self.delay)
        resp = self.session.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        return resp.text

    def _build_search_url(self, query: str):
        encoded_query = quote(query, safe='')
        search_path = f"{self.BASE_URL}/{self.region}/sell_spare_parts/+/{encoded_query}/"
        params = {'query': query}
        return search_path, params

    def get_image_and_shop_url(self, part_name: str, brand: str = None, model: str = None) -> tuple[str, str]:
        if not part_name:
            return None, None

        search_terms = [part_name]
        if brand:
            search_terms.append(brand)
        if model:
            search_terms.append(model)
        search_query = ' '.join(search_terms).strip()

        search_url, params = self._build_search_url(search_query)
        try:
            html = self._get(search_url, params=params)
        except Exception as e:
            print(f"[Ошибка поиска] {search_query}: {e}")
            return None, None

        soup = BeautifulSoup(html, 'html.parser')

        link = None
        selectors = [
            'a.bulletinLink',
            'a.bulletin-item__link',
            '.bulletinItem a',
            '.bulletin-list .bulletin-item a',
            'a[data-ftr-event="click"]'
        ]
        for sel in selectors:
            elem = soup.select_one(sel)
            if elem and elem.get('href'):
                link = elem['href']
                break

        if not link:
            for a in soup.find_all('a', href=True):
                if '/sell_spare_parts/' in a['href'] and 'page=' not in a['href']:
                    link = a['href']
                    break

        if not link:
            print(f"[Не найдено объявлений] {search_query}")
            return None, None

        shop_url = urljoin(self.BASE_URL, link)

        try:
            html = self._get(shop_url)
        except Exception as e:
            print(f"[Ошибка загрузки] {shop_url}: {e}")
            return None, shop_url

        soup = BeautifulSoup(html, 'html.parser')

        photo_url = None
        meta = soup.select_one('meta[property="og:image"]')
        if meta and meta.get('content'):
            photo_url = meta['content']
        if not photo_url:
            img = soup.select_one('.gallery__photo-img img, .image-container img, .bulletin-image img')
            if img:
                photo_url = img.get('src') or img.get('data-src')
        if not photo_url:
            img = soup.select_one('img[data-src]')
            if img:
                photo_url = img['data-src']
        if not photo_url:
            img = soup.select_one('img.photo')
            if img:
                photo_url = img.get('src')

        if photo_url and not photo_url.startswith('http'):
            photo_url = urljoin(self.BASE_URL, photo_url)

        return photo_url, shop_url