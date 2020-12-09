# Install all the tools.
import pymysql


# Call procedure sp_chart_v1 from dbase yahoo.
def call_procedure(connect_call_input=None, sql_call_input='procedure_test_01',
                   value_input_01=None, value_input_02=None):
    if connect_call_input is None:
        connect_call_input = pymysql.connect(
            user="****",
            password="****",
            host="localhost",
            port=3306,
            db="yahoo",
            charset="utf8"
        )
    else:
        connect_call_input = connect_call_input
        
    crr_call = connect_call_input.cursor()   
    crr_call.callproc(sql_call_input, (value_input_01, value_input_02))
    crr_call.close()
    connect_call_input.commit()