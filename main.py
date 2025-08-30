import os
from config import DATA_FOLDER
from data_handle import export_category
from books_scraper import get_all_pages, get_categories
import asyncio

os.makedirs(DATA_FOLDER, exist_ok=True)


async def process_category(category:tuple) -> None:
    category_name, category_link = category
    print(f"-----------Empezando categoria---------------")
    books_info = await get_all_pages(category_link)
    export_category(category_name, books_info)
    print(f"-----------Terminando categoria--------------")
    
    
    
async def main():
    categories = get_categories()[1::]
    processes = [process_category(category) for category in categories]
    await asyncio.gather(*processes)
        
        
if __name__ == "__main__":
    asyncio.run(main())
