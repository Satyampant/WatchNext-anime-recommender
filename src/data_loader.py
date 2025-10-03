import pandas as pd
from utils.logger import get_logger

logger = get_logger(__name__)
class AnimeDataLoader:
    def __init__(self, original_csv:str, processed_csv:str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        df = pd.read_csv(self.original_csv, encoding='utf-8', on_bad_lines='skip').dropna()
        
        # Filter out rows where English name is "Unknown" (case-insensitive)
        df = df[df["English name"].notna()]
        df = df[~df["English name"].str.upper().isin(["UNKNOWN", ""])]
        df = df[df["English name"].str.strip() != ""]
        
        logger.info(f"Rows after filtering 'Unknown': {len(df)}")
        
        df['combined_info'] = (
            "Title: " + df["English name"] + "\n"
            "Genres: " + df["Genres"] + "\n"
            "Synopsis: " + df["Synopsis"]
        )
        
        # Rename columns instead of creating new ones
        df = df.rename(columns={
            'Image URL': 'image_url',
            'English name': 'title'
        })
        
        output_df = df[["combined_info", "title", "image_url"]]
        output_df.to_csv(self.processed_csv, index=False, encoding='utf-8')
        
        return self.processed_csv