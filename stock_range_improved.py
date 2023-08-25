import datetime
import finplot as fplt
import tushare as ts
import pandas as pd
from datetime import date
import logging

# Initialize the Tushare API
pro = ts.pro_api('4b086ac94db69bf94c232743717ba838fab2f00528050ce2567cfb3a')

date_yesterday = date.today() - datetime.timedelta(days=1)
str_yesterday = date_yesterday.strftime('%Y%m%d')

# Initialize logging
logging.basicConfig(filename='stock_range_improve.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    ts_code = input('Please enter the ts code: ')
    end_date = input('Please enter the end date: ')
    time_delta = int(input('Please enter the time delta: '))
    return ts_code, end_date, time_delta


def fetch_and_process_data(ts_code_in='002027.SZ', year_del_in=1, end_date_in=str_yesterday,
                           fetch_func_in=pro.stk_factor):
    """
    Fetches and processes data.

    Parameters:
    ts_code_in (str): The ts code.
    year_del_in (int): The year del.
    end_date_in (str): The end date.
    fetch_func_in (function): The fetch function.

    Returns:
    DataFrame: The processed data.
    """
    try:
        # Calculate start date based on year delta
        start_date = date.today() - datetime.timedelta(weeks=52 * year_del_in) - datetime.timedelta(days=1)
        str_start_date = start_date.strftime('%Y%m%d')

        # Fetch data using the provided function
        df = fetch_func_in(ts_code=ts_code_in, start_date=str_start_date, end_date=end_date_in)

        # Rename 'vol' column to 'volume'
        df = df.rename(columns={'vol': 'volume'})

        # Convert 'trade_date' column to datetime format and set it as the index
        df['trade_date'] = pd.to_datetime(df['trade_date'], format='%Y%m%d')
        df.set_index('trade_date', inplace=True)

        # Sort DataFrame by date
        df.sort_index(inplace=True)

        logger.info(f"Data fetched and processed successfully for {ts_code_in}")
        return df

    except Exception as e:
        logger.error(f"Error fetching and processing data for {ts_code_in}: {e}")
        return None


def stock_qfq_daily(ts_code_in='002027.SZ', year_delta=1, end_date_in=str_yesterday):
    return fetch_and_process_data(ts_code_in, year_delta, end_date_in, pro.stk_factor)


def stock_mx(ts_code_in='002027.SZ', year_delta=1, end_date_in=str_yesterday):
    return fetch_and_process_data(ts_code_in, year_delta, end_date_in, pro.stock_mx)


def stock_cyq_perf(ts_code_in='002027.SZ', year_delta=1, end_date_in=str_yesterday):
    return fetch_and_process_data(ts_code_in, year_delta, end_date_in, pro.cyq_perf)


def calculate_macd(df, short_span=12, long_span=26, fillna=False):
    """
    Calculate MACD (Moving Average Convergence Divergence) for a given DataFrame.

    Parameters:
    df (DataFrame): Input DataFrame with 'close' prices.
    short_span (int): Short span for EMA calculation. Default is 12.
    long_span (int): Long span for EMA calculation. Default is 26.
    fillna (bool): If True, fill NaN values with 0. Default is False.

    Returns:
    DataFrame: DataFrame with MACD values.
    """
    try:
        EMA12 = df['close'].ewm(span=short_span, adjust=False).mean()
        EMA26 = df['close'].ewm(span=long_span, adjust=False).mean()
        MACD_Line = EMA12 - EMA26
        Signal_Line = MACD_Line.ewm(span=9, adjust=False).mean()
        MACD_Hist = MACD_Line - Signal_Line
        df = df.assign(MACD_Line=MACD_Line, Signal_Line=Signal_Line, MACD_Hist=MACD_Hist)

        # Fill NaN values if fillna is set to True
        if fillna:
            df = df.fillna(0)

        logger.info("MACD calculated successfully.")
        return df

    except Exception as e:
        logger.error(f"Error calculating MACD: {e}")
        return None


def color_k(y_input):
    """
    Define a color function that colors positive values green and negative values red.

    Parameters:
    y_input (list): List of values.

    Returns:
    list: List of colors corresponding to the input values.
    """
    try:
        colors = ['#143605' if y < 0 else '#7bf2da' for y in y_input]
        logger.info("Colors generated successfully.")
        return colors

    except Exception as e:
        logger.error(f"Error generating colors: {e}")
        return None


if __name__ == '__main__':
    data_in = main()
    ts_code = data_in[0]
    end_date = data_in[1]
    time_delta = data_in[2]
    # ts_code = input('Give me the stock code like xxxxxx.SH/xxxxxx.SZ. ')
    # end_date = input('Give me the ending date.')
    # ts_code = input("Please provide stock code ends with .SH or .SZ: ")
    # end_date = input("Please provide ending_date: ")
    # time_delta = input('How long would you like me to review? ')
    df_stock = stock_qfq_daily(ts_code_in=ts_code, year_delta=time_delta, end_date_in=end_date)
    df_cyq = stock_cyq_perf(ts_code_in=ts_code, year_delta=time_delta, end_date_in=end_date)
    df_stock_mx = stock_mx(ts_code_in=ts_code, year_delta=time_delta, end_date_in=end_date)
    # df_stock_mx['mx_grade'] = 2.5 - df_stock_mx['mx_grade']
    # print(df_stock, df_cyq, df_stock_mx)

    ax, ax2, ax3, ax4 = fplt.create_plot("'" + ts_code + "'", rows=4)

    # plot macd with standard colors first
    macd = df_stock.close.ewm(span=12).mean() - df_stock.close.ewm(span=26).mean()
    signal = macd.ewm(span=9).mean()
    df_stock['macd_diff'] = macd - signal
    fplt.volume_ocv(df_stock[['open_qfq', 'close_qfq', 'macd_diff']], ax=ax2, colorfunc=fplt.strength_colorfilter)
    fplt.plot(macd, ax=ax2, legend='MACD')
    fplt.plot(signal, ax=ax2, legend='Signal')

    # change to b/w coloring templates for next plots
    # fplt.candle_bull_color = fplt.candle_bear_color = fplt.candle_bear_body_color = '#000'
    # fplt.volume_bull_color = fplt.volume_bear_color = '#333'
    # fplt.candle_bull_body_color = fplt.volume_bull_body_color = '#fff'
    # fplt.candlestick_ochl(df_stock[['open', 'close', 'high', 'low']])

    fplt.candlestick_ochl(df_stock[['open_qfq', 'close_qfq', 'high_qfq', 'low_qfq']], ax=ax,
                          colorfunc=fplt.strength_colorfilter)
    hover_label = fplt.add_legend('{0} - {1} - {2} Years'.format(ts_code, end_date, time_delta), ax=ax)
    axo = ax.overlay()
    fplt.volume_ocv(df_stock[['open_qfq', 'close_qfq', 'volume']], ax=axo)
    fplt.plot(df_stock.volume.ewm(span=24).mean(), ax=axo, color=1)

    processing_point = df_cyq['cost_50pct'] - df_cyq['weight_avg']
    trigger_point = processing_point
    fplt.plot(trigger_point, ax=ax3, legend='cost_50pct - weighted_avg')

    mx_columns = [('mx_grade', '#0c1793'),
                  ('com_stock', '#ff028d'),
                  ('zt_sum_z', '#0ffef9'),
                  ('wma250_z', '#40fd14')]

    """for column, color in mx_columns:
        df_stock_mx[column].plot(ax=ax4, color=color, legend=column)"""

    cost_columns = [('cost_5pct', '#e4cbff'),
                    ('cost_15pct', '#c79fef'),
                    ('cost_50pct', '#ca9bf7'),
                    ('weight_avg', '#ff08e8'),
                    ('cost_85pct', '#a55af4'),
                    ('cost_95pct', '#380282')]

    for column, color in cost_columns:
        df_cyq[column].plot(ax=ax, color=color)


    def save():
        fplt.screenshot(
            open('E:/Picture/Stock Chart Generation/{0}-{1}-{2}.png'.format(ts_code, end_date, str(time_delta)), 'wb'))


    fplt.timer_callback(save, 0.5, single_shot=True)  # wait some until we're rendered

    fplt.show()
