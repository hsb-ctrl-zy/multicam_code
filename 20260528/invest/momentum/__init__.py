import pandas as pd
import numpy as np
from datetime import datetime

def create_ym(_df, _col = 'Adj Close'):
    df = _df.copy()
    # Date가 column에 포함되어 있는가?
    if 'Date' in df.columns:
        df.set_index('Date', inplace = True)
    df.index = pd.to_datetime(df.index)
    df.index = df.index.tz_localize(None)
    flag = df.isin([np.nan, np.inf, -np.inf]).any(axis=1)
    df = df.loc[~flag, [_col]]
    df['STD-YM'] = df.index.strftime('%Y-%m')

    return df

def create_month(
        _df,
        _start = '2010-01-01',
        _end = datetime.now(),
        _momentum = 12,
        _last = 1
):

    if _last == 1:
        df = _df.groupby('STD-YM').tail(1)
    elif _last == 0:
        df = _df.groupby('STD-YM').head(1)
    else:
        return "_last 값은 0 또는 1만 가능합니다."
    
    col = _df.columns[0]

    df['BF1'] = df.shift(1)[col].fillna(0)
    df['BF2'] = df.shift(_momentum)[col].fillna(0)
    
    df = df.loc[ _start : _end, ]
    return df

def create_trade_rtn(_df1, _df2, _score = 1):
    df = _df1.copy()

    df['trade'] = ''
    df['rtn'] = 1.0

    col = df.columns[0]

    # _df2를 이용해서 거래 내역을 생성
    for i in _df2.index:
        signal = ''
        
        # momentum 계산
        momentum_index = _df2.loc[i, 'BF1'] / _df2.loc[i, 'BF2'] - _score
        flag = (momentum_index > 0) & (momentum_index != np.inf)
        
        if flag:
            signal = 'buy'
        
        # 거래 내역 생성
        df.loc[i:, 'trade'] = signal
        print(f'날짜: {i}, momentum_index: {momentum_index}, signal: {signal}')
    
    # 수익률 계산
    for i in df.index:
        if (df.shift(1).loc[i, 'trade'] == '') & (df.loc[i, 'trade'] == 'buy'):
            buy = df.loc[i, col]
            print(f'매수일: {i}, 매수가: {buy}')
        elif (df.shift(1).loc[i, 'trade'] == 'buy') & (df.loc[i, 'trade'] == ''):
            sell = df.loc[i, col]
            rtn = sell / buy
            df.loc[i, 'rtn'] = rtn
            print(f'매도일: {i}, 매도가: {sell}, 수익률: {rtn}')
    
    # 누적 수익률 계산
    df['acc_rtn'] = df['rtn'].cumprod()
    acc_rtn = df.iloc[-1, -1]

    return df, acc_rtn