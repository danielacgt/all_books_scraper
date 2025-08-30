from bs4 import BeautifulSoup
from curl_cffi import requests, AsyncSession

ROOT = "https://books.toscrape.com"

def make_requests(url:str) -> requests.Response: 
    response = requests.get(url)
    return response  

def get_categories() -> list:
    print("Getting categories")
    response_books = make_requests(ROOT)
    soup = BeautifulSoup(response_books.text, "html.parser")
    categories_list = []
    categories = soup.select("div.side_categories a")
    for category in categories:
        name_category = category.text.strip()
        link = category["href"].replace("index.html","").strip()
        tupla = (name_category, link)
        categories_list.append(tupla)
    print("Got categories")
    return categories_list


def get_info(response:requests.Response) -> list:
    soup = BeautifulSoup(response.text, "html.parser")
    lista_fichas = []
    fichas = soup.select("li.col-xs-6.col-sm-4.col-md-3.col-lg-3")
    for ficha in fichas:
        ficha_dict = {}
        ficha_dict["titulo"] = ficha.select_one("h3 a")["title"]
        ficha_dict["price"] = ficha.select_one("div p.price_color").text
        ficha_dict["rating"] = ficha.select_one("article p")["class"][1]
        lista_fichas.append(ficha_dict)
    return lista_fichas

async def get_all_pages(url:str) -> list:
    num = 1
    info_pages = []
    async with AsyncSession() as session:
        while True:
            fixed_url = f"{ROOT}/{url}" if num == 1 else f"{ROOT}/{url}page-{num}.html"
            print(f"scraping link: {fixed_url}")
            response_pages = await session.get(fixed_url)
            if response_pages.status_code != 200:
                break
            info_page = get_info(response_pages)
            info_pages.extend(info_page)
            num += 1
    return info_pages
    

        
if __name__ == "__main__":
    name_category, link_category = get_categories()[2]
    books_info = get_all_pages(link_category)
    print(books_info)
    print(len(books_info))
