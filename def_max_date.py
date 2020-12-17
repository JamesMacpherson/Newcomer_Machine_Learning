connect = pymysql.connect(
    user="root",
    password="root",
    host="***.***.***.***",
    port=3306,
    db="stock_cn",
    charset="utf8"
)

# Get the max date + 1 in the db / table (like stock_cn / money_flow) for additional data input from tu_share. 
def max_date(stk, conn=connect):
    sql_max_date = 'SELECT MAX(trade_date) date_max FROM money_flow WHERE ts_code = "{0}"'.format(stk)
    date_max_str = pd.read_sql(sql_max_date, conn)
    date_max_pro = datetime.datetime.strptime(date_max_str['date_max'][0], '%Y%m%d')
    date_max_stamp = date_max_pro + datetime.timedelta(days=1)
    date_max = datetime.datetime.strftime(date_max_stamp, '%Y%m%d')
    return date_max
