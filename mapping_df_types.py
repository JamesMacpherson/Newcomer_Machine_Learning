# Install all the tools.
import sqlalchemy as aqm


def mapping_df_types(df_input):
    dtypedict = {}
    for i, j in zip(df_input.columns, df_input.dtypes):
        if 'object' in str(j):
            dtypedict.update({i: aqm.NVARCHAR(length=255)})
        if 'float' in str(j):
            dtypedict.update({i: aqm.Float(precision=2, asdecimal=True)})
        if 'int' in str(j):
            dtypedict.update({i: aqm.Integer()})
    return dtypedict