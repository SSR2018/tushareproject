import tushare as ts
"""""
token :token
ts_code:股票代码
start_date :起始日期
end_date:终止日期
"""""
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
    爬去输出参数的中英文
    """""
    def spyder(self,id_num):
        url = 'https://tushare.pro/document/2?doc_id='+str(id_num)
        import requests
        headers = headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
        t = requests.get(url = url,headers = headers)
        t.encoding = t.apparent_encoding
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(t.text, 'html.parser')

        if '默认' in str(soup):
            l = 4
        else:
            l = 3

        s = soup.find_all('table')[1].find_all('td')
        out_dict = dict()
        for num in range(len(s)//l):
            out_dict[s[l*num].text] = s[l*num+l-1].text
        return out_dict
    def col2(self,id_num,data):
        dict = self.spyder(id_num = id_num)
        list = []
        for col in data.columns:
            list.append(dict[col])
        data.columns = list
        return data

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
        #sb_dict = {'ts_code': 'TS代码', 'symbol': '股票代码', 'name': '股票名称', 'area': '所在地域', 'industry': '所属行业', 'fullname': '股票全称'\
        #              , 'enname': '英文名称', 'market': '市场类型', 'curr_type': '交易货币', 'list_status': '上市状态', 'delist_date': '退市日期'\
        #             , 'list_date': '上市日期', 'is_hs': '是否沪深港通标的'}
        sb_dict = self.spyder( id_num =25)
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
    """""
    股票曾用名
    
    名称	类型	必选	描述
    ts_code	str	N	TS代码
    start_date	str	N	公告开始日期
    end_date	str	N	公告结束日期
    ts_code	str	Y	TS代码
    name	str	Y	证券名称
    start_date	str	Y	开始日期
    end_date	str	Y	结束日期
    ann_date	str	Y	公告日期
    change_reason	str	Y	变更原因
    """""
    def namechange(self,fields = ''):
        if fields != '':
            nc = self.pro.namechange(ts_code = self._ts_code,start_date = self.start_date,end_date = self.end_date,fields = fields)
        else:
            nc = self.pro.namechange(ts_code =self._ts_code,start_date = self.start_date,end_date = self.end_date)
        nc_dict = {'ts_code':'TS代码','name':'证券名称','start_date':'开始日期','end_date':'结束日期','ann_date':'公告日期','change_reason':'变更原因'}
        nc_list = []
        for col_nc in nc.columns:
            nc_list.append(nc_dict[col_nc])
        nc.columns = nc_list
        return nc
    """""
    沪深股通成份股
    接口：hs_const
    描述：获取沪股通、深股通成分数据
    名称	类型	必选	描述
    hs_type	str	Y	类型SH沪股通SZ深股通
    is_new	str	N	是否最新 1 是 0 否 (默认1)
    类型	默认显示	描述
    ts_code	str	Y	TS代码
    hs_type	str	Y	沪深港通类型SH沪SZ深
    in_date	str	Y	纳入日期
    out_date	str	Y	剔除日期
    is_new	str	Y	是否最新 1是 0否
    """""
    def hs_const(self,hs_type = 'SH',is_new = ''):
        hs = self.pro.hs_const(hs_type=hs_type,is_new = is_new)
        hs = self.col2(id_num = 104,data = hs)
        return hs
    """""
    接口：stock_company
    描述：获取上市公司基础信息
    积分：用户需要至少120积分才可以调取，具体请参阅积分获取办法
    
    输入参数
    
    名称	类型	默认显示	描述
    exchange	str	N	交易所代码 ，SSE上交所 SZSE深交所 ，默认SSE
    输出参数
    """""
    def stoc_company(self,exchange = '',fields = ''):
        if len(fileds) ==0 :
            sc = self.pro.stock_company(exchange= exchagne)
        else:
            sc = self.pro.stock_compnay(exchange = exchange , fields = fields)
        sc = self.col2(id_num = 112,data =sc)
        return sc
    """""
    IPO新股列表
    接口：new_share
    描述：获取新股上市列表数据
    限量：单次最大2000条，总量不限制
    积分：用户需要至少120积分才可以调取，具体请参阅积分获取办法
    
    输入参数
    
    名称	类型	必选	描述
    start_date	str	N	上网发行开始日期
    end_date	str	N	上网发行结束日期
    """""
    def IPO(self,start_date = self.start_date,end_date = self.end_date):
        ipo = self.pro.new_share(start_date=start_date, end_date=end_date)
        ipo = self.col2(id_num = 123 ,data =ipo)
        return ipo
T = Tushare_data()

print(T.hs_const())
