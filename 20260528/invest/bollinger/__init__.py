import numpy as np
from datetime import datetime
import pandas as pd

def create_band(
        _df,
        _col = 'Adj Close',
        _start = '2010-01-01',
        _end = datetime.now(),
        _cnt = 20
):
    
    df = _df.copy()

    if 'Date' in df.columns:
        df.set_index('Date', inplace=True)
    
    df.index = pd.to_datetime(df.index)

    df.index = df.index.tz_localize(None)

    flag = df.isin( [ np.nan, np.inf, -np.inf ] ).any(axis=1)
    df = df.loc[~flag, ]

    df = df[[_col]]

    df['center'] = df[_col].rolling(_cnt).mean()

    std_value = 2 * df[_col].rolling(_cnt).std()
    df['ub'] = df['center'] + std_value
    df['lb'] = df['center'] - std_value

    df = df.loc[_start:_end, ]

    return df

def create_trade(_df):
    # 기준 컬럼 이름을 어떻게 알 것인가?: 첫번째 함수의 return으로 나온 df의 첫번째 컬럼만
    col = _df.columns[0]
    df = _df.copy()
    df['trade'] = ''

    for i in df.index:
        if df.loc[i, col] >= df.loc[i, 'ub']:
            # 매도
            df.loc[i, 'trade'] = ''
        elif df.loc[i, col] <= df.loc[i, 'lb']:
            # 매수
            df.loc[i, 'trade'] = 'buy'
        else:
            if df.shift().loc[i, 'trade'] == 'buy':
                df.loc[i, 'trade'] = 'buy'
            else:
                df.loc[i, 'trade'] = ''
    
    return df

def create_rtn(_df):
    col = _df.columns[0]
    df = _df.copy()
    
    df['rtn'] = 1.0

    # 수익률 계산
    for i in df.index:
        # 매수
        if (df.shift().loc[i, 'trade'] == '') & (df.loc[i, 'trade'] == 'buy'):
            buy = df.loc[i, col]
            print(f"매수일: {i}, 매수가: {buy}")
            print()
        elif (df.shift().loc[i, 'trade'] == 'buy') & (df.loc[i, 'trade'] == ''):
            sell = df.loc[i, col]
            rtn = sell / buy
            df.loc[i, 'rtn'] = rtn
            print(f"매도일: {i}, 매도가: {sell}, 수익률: {rtn}")
            print()
    # 누적 수익률
    df['acc_rtn'] = df['rtn'].cumprod()
    # 최종 수익률
    acc_rtn = df.iloc[-1, -1]

    return df, acc_rtn