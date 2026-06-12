import pandas as pd
from datetime import datetime

if __name__ == '__main__':
    from bollinger import create_band, create_trade, create_rtn
    from momentum import create_ym, create_month, create_trade_rtn
else:
    from invest.bollinger import create_band, create_trade, create_rtn
    from invest.momentum import create_ym, create_month, create_trade_rtn

class Investing():
    def __init__(self, _df, _col = 'Adj Close', _start = '2010-01-01', _end = datetime.now()):
        self.df = _df
        self.col = _col
        self.start = _start
        self.end = _end
    
    # 바이앤홀드 함수
    def bnh(self):
        df = self.df.copy()
        if 'Date' in df.columns:
            df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index)
        df.index = df.index.tz_localize(None)
        df = df.loc[self.start:self.end, [self.col]]
        buy = df.iloc[0, 0]
        sell = df.iloc[-1, 0]
        return sell / buy
    
    # 볼린져 밴드 함수
    def boll(self, _cnt = 20):
        band_df = create_band(self.df, self.col, self.start, self.end, _cnt)
        trade_df = create_trade(band_df)
        rtn_df, acc_rtn = create_rtn(trade_df)
        return rtn_df, acc_rtn
    
    # 절대 모멘텀 함수
    def mmt(self, _momentum = 12, _score = 1, _last = 1):
        df = self.df.copy()
        ym_df = create_ym(df, self.col)
        month_df = create_month(ym_df, self.start, self.end, _momentum, _last)
        rtn_df, acc_rtn = create_trade_rtn(ym_df, month_df, _score)
        return rtn_df, acc_rtn

# 모듈 테스트 코드
if __name__ == '__main__':
    df = pd.read_csv('../../csv/MSFT.csv')
    invest = Investing(df)
    rtn_df, acc_rtn = invest.mmt()
    print(rtn_df)
    print(acc_rtn)