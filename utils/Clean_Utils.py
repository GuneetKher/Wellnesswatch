import pandas as pd
import re
class Clean_Utils:
    def keep_words_gt_n(self,df: pd.DataFrame,n:int) -> pd.DataFrame:
        count_words = lambda text: len(text.split())
        mask = df['Text'].apply(count_words) > n
        return df[mask]

    def remove_links(self,text:str) -> str:
        text = re.sub(r'http\S+', '', text)
        return text
    def remove_newline(self,text:str) -> str:
        text = text.replace('\n\n', '\n')  
        text = text.replace('\n', '.')  
        return text
