import tushare as ts
class Tushare_data:
    def __init__(self,ts_code ='',start_date ='',end_date = ''):
        self._token =  'e8df84bd1b25a8a2a2ceb7edf7ad41f2c3a1d3ec604bb8abd40321f4'
        self.pro = ts.pro_api(self._token)
        self._ts_code = ts_code
        self.start_date = start_date
        self.end_date = end_date
    """""
    print the version of the tushare
    """""
    def ts_version(self):
        print('The version of the tushare is {}'.format(ts.__version__))
    """""
    shibor
    libor
    hibor
    lpr:LPR贷款基础利率
    """""
    def shibor(self,date = ''):
        if date == '':
            return self.pro.shibor(start_date = self.start_date,end_date = self.end_date)
        else:
            return self.pro.shibor(date = date)
    def libor(self,date = ''):
        if date == '':
            return self.pro.hibor(start_date = self.start_date ,end_date = self.end_date,curr_type ='')
        else:
            return self.pro.hibor(date = date)
    def hibor(self,date =''):
        if date == '':
            return self.pro.hibor(start_date=self.start_date, end_date=self.end_date)
        else:
            return self.pro.hibor(date = date)
    def lpr(self,date = ''):
        if date == '':
            return self.pro.shibor_lpr(start_date=self.start_date, end_date=self.end_date)
        else:
            return self.pro.shibor_lpr(date = date)
    """""
    stock_basic:股票列表
    is_hs :是否沪深港通标的，N否 H沪股通 S深股通
    上市状态： L上市 D退市 P暂停上市
    交易所 SSE上交所 SZSE深交所 HKEX港交所(未上线)
    ts_code	str	TS代码
    symbol	str	股票代码
    name	str	股票名称
    area	str	所在地域
    industry	str	所属行业
    fullname	str	股票全称
    enname	str	英文全称
    market	str	市场类型 （主板/中小板/创业板）
    exchange	str	交易所代码
    curr_type	str	交易货币
    list_status	str	上市状态： L上市 D退市 P暂停上市
    list_date	str	上市日期
    delist_date	str	退市日期
    is_hs	str	是否沪深港通标的，N否 H沪股通 S深股通
    """""
    def stock_basic(self,is_hs ='N',list_status = 'L',exchange = '',fields = ''):
        if len(fields) == 0:
            sb = self.pro.stock_basic(is_hs = is_hs,exchange=exchange, list_status=list_status)
        else:
            sb = self.pro.stock_basic(is_hs = is_hs,exchange=exchange, list_status=list_status,fields = fields)
        sb_dict = {'ts_code': 'TS代码', 'symbol': '股票代码', 'name': '股票名称', 'area': '所在地域', 'industry': '所属行业', 'fullname': '股票全称'\
                      , 'enname': '英文名称', 'market': '市场类型', 'curr_type': '交易货币', 'list_status': '上市状态', 'delist_date': '退市日期'\
                      , 'list_date': '上市日期', 'is_hs': '是否沪深港通标的'}
        sb_list = []
        for col_sb in sb.columns:
            sb_list.append(sb_dict[col_sb])
        sb.columns = sb_list
        return sb
    """""
    交易日历:获取各大交易所交易日历数据
    exchange	str	N	交易所 SSE上交所 SZSE深交所
    start_date	str	N	开始日期
    end_date	str	N	结束日期
    is_open	str	N	是否交易 '0'休市 '1'交易
    exchange	str	Y	交易所 SSE上交所 SZSE深交所
    cal_date	str	Y	日历日期
    is_open	str	Y	是否交易 0休市 1交易
    pretrade_date	str	N	上一个交易日
    """""
    def trade_cal(self,exchange = '',is_open =''):
        tc = self.pro.trade_cal(exchange=exchange, start_date=self.start_date, end_date=self.end_date,is_open = is_open)
        tc_dict = {'exchange':'交易所','cal_date':'日历日期','is_open':'是否交易','pretrade_date':'上一个交易日'}
        tc_list = []
        for col_tc in tc.columns:
            tc_list.append(tc_dict[col_tc])
        tc.columns = tc_list
        return tc
T = Tushare_data()
print(T.trade_cal())

