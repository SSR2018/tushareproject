import tushare as ts
import numpy as np
import pandas as pd
from pyecharts.charts import Kline,Bar,Grid,Line
from pyecharts import options as opts

class MyTushare:
    def __init__(self,token):
        ts.set_token(token)
        self._pro = ts.pro_api()
    def stock_basic(self):
        return self._pro.stock_basic(exchange='',list_status= 'L')
    def calculate_ma(self,data,ma):
        return pd.Series.rolling(data,window = ma).mean()
    def _draw_kline(self,name,df):
        assert type(name) is str,'The name should be a string'
        assert (type(df) is pd.DataFrame) and (df.shape[1] == 6), \
            'The df should be a 6 columns (date , open, close, low, high , vol) DataFrame'
        date = df.trade_date.values.tolist()
        klineData =df[['open','close','low','high']].values.tolist()
        volume = []
        for ix in range(len(df)):
            volume.append([ix,df.vol[ix],1 if df.close[ix] > df.open[ix] else -1])
        #K Line
        kline = (
            Kline()
                .add_xaxis(xaxis_data=date)
                .add_yaxis(
                series_name="Dow-Jones index",
                y_axis=klineData,
                itemstyle_opts=opts.ItemStyleOpts(color="#ec0000", color0="#00da3c"),
            )
                .set_global_opts(
                legend_opts=opts.LegendOpts(
                    is_show=False, pos_bottom=10, pos_left="center"
                ),
                datazoom_opts=[
                    opts.DataZoomOpts(
                        is_show=False,
                        type_="inside",
                        xaxis_index=[0, 1],
                        range_start=70,
                        range_end=100,
                    ),
                    opts.DataZoomOpts(
                        is_show=True,
                        xaxis_index=[0, 1],
                        type_="slider",
                        pos_top="85%",
                        range_start=98,
                        range_end=100,
                    ),
                ],
                yaxis_opts=opts.AxisOpts(
                    is_scale=True,
                    splitarea_opts=opts.SplitAreaOpts(
                        is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
                    ),
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="axis",
                    axis_pointer_type="cross",
                    background_color="rgba(245, 245, 245, 0.8)",
                    border_width=1,
                    border_color="#ccc",
                    textstyle_opts=opts.TextStyleOpts(color="#000"),
                ),
                visualmap_opts=opts.VisualMapOpts(
                    is_show=False,
                    dimension=2,
                    series_index=5,
                    is_piecewise=True,
                    pieces=[
                        {"value": 1, "color": "#00da3c"},
                        {"value": -1, "color": "#ec0000"},
                    ],
                ),
                axispointer_opts=opts.AxisPointerOpts(
                    is_show=True,
                    link=[{"xAxisIndex": "all"}],
                    label=opts.LabelOpts(background_color="#777"),
                ),
                brush_opts=opts.BrushOpts(
                    x_axis_index="all",
                    brush_link="all",
                    out_of_brush={"colorAlpha": 0.1},
                    brush_type="lineX",
                ),
            )
        )

        line = (
            Line()
                .add_xaxis(xaxis_data=date)
                .add_yaxis(
                series_name="MA5",
                y_axis=self.calculate_ma(data=df.close,ma=5).values.tolist(),
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                series_name="MA10",
                y_axis=self.calculate_ma(data=df.close,ma=10).values.tolist(),
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                series_name="MA20",
                y_axis=self.calculate_ma(data=df.close,ma=20).values.tolist(),
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
                .add_yaxis(
                series_name="MA60",
                y_axis=self.calculate_ma(data=df.close,ma=60).values.tolist(),
                is_smooth=True,
                is_hover_animation=False,
                linestyle_opts=opts.LineStyleOpts(width=3, opacity=0.5),
                label_opts=opts.LabelOpts(is_show=False),
            )
                .set_global_opts(xaxis_opts=opts.AxisOpts(type_="category"))
        )

        bar = (
            Bar()
                .add_xaxis(xaxis_data=date)
                .add_yaxis(
                series_name="Volume",
                y_axis=volume,
                xaxis_index=1,
                yaxis_index=1,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    is_scale=True,
                    grid_index=1,
                    boundary_gap=False,
                    axisline_opts=opts.AxisLineOpts(is_on_zero=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    split_number=20,
                    min_="dataMin",
                    max_="dataMax",
                ),
                yaxis_opts=opts.AxisOpts(
                    grid_index=1,
                    is_scale=True,
                    split_number=2,
                    axislabel_opts=opts.LabelOpts(is_show=False),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(is_show=False),
                    splitline_opts=opts.SplitLineOpts(is_show=False),
                ),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

        # Kline And Line
        overlap_kline_line = kline.overlap(line)

        # Grid Overlap + Bar
        grid_chart = Grid(
            init_opts=opts.InitOpts(
                width="1000px",
                height="800px",
                animation_opts=opts.AnimationOpts(animation=False),
            )
        )
        grid_chart.add(
            overlap_kline_line,
            grid_opts=opts.GridOpts(pos_left="10%", pos_right="8%", height="50%"),
        )
        grid_chart.add(
            bar,
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

if __name__ == "__main__":
    mt = MyTushare(token = 'e8df84bd1b25a8a2a2ceb7edf7ad41f2c3a1d3ec604bb8abd40321f4')
    data = mt.daily(ts_code='300001.SZ', start_date='20190701', end_date='20200701',drawkline=True)