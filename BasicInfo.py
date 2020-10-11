import tushare as ts
import numpy as np
import pandas as pd
from pyecharts.charts import Kline,Bar,Grid
from pyecharts import options as opts

class MyTushare:
    def __init__(self,token):
        ts.set_token(token)
        self._pro = ts.pro_api()
    def stock_basic(self):
        return self._pro.stock_basic(exchange='',list_status= 'L')
    def _draw_kline(self,name,df):
        assert type(name) is str,'The name should be a string'
        assert (type(df) is pd.DataFrame) and (df.shape[1] == 6), \
            'The df should be a 6 columns (date , open, close, low, high , vol) DataFrame'
        kline = Kline()
        kline.add_xaxis(df.iloc[:,0].values.tolist())
        kline.add_yaxis(f'{name}',df.iloc[:,1:-1].values.tolist())
        vol = Bar()
        vol.add_xaxis(df.iloc[:,0].values.tolist())
        vol.add_yaxis(f'{name}',df.iloc[:,-1].values.tolist(),label_opts=opts.LabelOpts(is_show=False))
        grid_chart = Grid(
            init_opts=opts.InitOpts(
                width="1000px",
                height="800px",
                animation_opts=opts.AnimationOpts(animation=False),
            )
        )
        grid_chart.add(
            kline,
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
        )
        grid_chart.add(
            vol,
            grid_opts=opts.GridOpts(
                pos_left="10%", pos_right="8%", pos_top="63%", height="16%"
            ),
        )

        grid_chart.render(f'{name}.html')
    def daily(self,ts_code,start_date,end_date,drawkline=True):
        df = self._pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
        if drawkline:
            self._draw_kline(name = ts_code,df = df[['trade_date','open','close','low','high','vol']][::-1])
            return df
        else:
            return df
mt = MyTushare(token = 'e8df84bd1b25a8a2a2ceb7edf7ad41f2c3a1d3ec604bb8abd40321f4')
print(mt.daily(ts_code='600000.SH', start_date='20180701', end_date='20190701'))