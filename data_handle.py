import pandas as pd
import os 
from config import DATA_FOLDER
#exportar la informacion como csv
def export_category(book_category:str, book_info:list):
    folder_path = f"{DATA_FOLDER}/{book_category}" #Porque se pasara el folder path nuevamente
    os.makedirs(folder_path, exist_ok=True)
    book_df = pd.DataFrame(book_info)
    book_df.to_csv(f"{folder_path}/{book_category}.csv")
    
