# Install all the tools.
import pandas as pd
from tqdm import tqdm


# Define the function to get stock list from local csv.
def stock_list_local(file_path='C:/Users/93761/PycharmProjects/test_study/stock_list_20201207.csv'):
    df = pd.read_csv(file_path)
    stocks = df['ts_code'].tolist()
    for stk in tqdm(stocks):
        print(stk)


if __name__ == '__main__':
    stock_list_local()