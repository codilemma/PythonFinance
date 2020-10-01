
from scipy.optimize import newton
import pandas as pd


df = pd.read_excel('../data/xirr.xlsx', sheet_name='regular')


# Net Present Value
# IRR/XIRR is tightly coupled with net present value (NPV/XNPV)
def xnpv(rate, values, dates):
    '''Replicates the excel XNPV() function'''
    min_date = min(dates)
    return sum([
        value / (1 + rate)**((date - min_date).days / 365)
        for value, date
        in zip(values, dates)
    ])

xnpv(0.05, df.total, df.date)

# Internal Rate of Return (IRR) Function

def xirr(values, dates):
    '''Replicates the excel XIRR() function'''
    return newton(lambda r: xnpv(r, values, dates), 0)


df['total'] = df.income + df.expenses
xirr(df.total, df.date)