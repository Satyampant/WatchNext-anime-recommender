import pandas as pd

class AnimeDataLoader:
    def __init__(self, original_csv:str, processed_csv:str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        df = pd.read_csv(self.original_csv, encoding='utf-8', on_bad_lines='skip').dropna()
        required_cols = ["English name", "Genres", "Synopsis"]

        df['combined_info'] = (
            "Title: " + df["English name"] + "\n"
            "Genres: " + df["Genres"] + "\n"
            "Synopsis: " + df["Synopsis"]
        )
        df['image_url'] = df['Image URL']
        df['title'] = df['English name']
        
        df[["combined_info", "title", "image_url"]].to_csv(self.processed_csv, index=False, encoding='utf-8')
        
        return self.processed_csv