'''
https://www.icbc-axa.com/axa/getUlPriceByType.do?ulType=1&year=2004&month=1&tb_switch=1
'''
# ulType(卓越/稳健/安心/进取：1/2/3/5)
# year(卓越/稳健/安心/进取：2003/2003/2003/2011)
# month(卓越/稳健/安心/进取：1/1/1/11)

from urllib import request, parse
import json
import time
import threading

class Gongyinansheng(object):
    url = r'https://www.icbc-axa.com/axa/getUlPriceByType.do'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Connection': 'keep-alive'
    }

    def __init__(self, ulType, year, month):
        self.ulType = ulType
        self.year = year
        self.month = month
        self.tb_switch = 1
        self.data = {
            'ulType': self.ulType,
            'year': self.year,
            'month': self.month,
            'tb_switch': self.tb_switch,
        }
        self.str_ym = str(ulType)+'_'+str(year)+'_'+str(month)
        self.get_data = {}


    def pashuju(self, data):
        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(self.url, headers=self.headers, data=data)
        html = request.urlopen(req).read()
        html = html.decode('utf-8')
        return html


    def loaddata(self, html):
        page_dict = json.loads(html)
        self.get_data[self.str_ym] = page_dict["ulData"]


    def getOneInfo(self):
        test = self.pashuju(self.data)
        self.loaddata(test)
        print(self.get_data)
        return self.get_data


# def main(ulType,year,month):
#     global tmp_dict
#     gyas = Gongyinansheng(ulType,year, month)
#     gyas_dict= gyas.getOneInfo()
#     if [] not in gyas_dict.values():
#         tmp_dict.update(gyas_dict)


# tmp_dict = {}
# for ulType in [1,2,3,5]:
#     for year in range(2003, 2018):
#         for month in range(1,13):
#             t = threading.Thread(target=main,args=(ulType,year,month,))
#             t.start()
#     time.sleep(2)
#
#
#
# with open('test.txt','w') as f:
#     f.write(json.dumps(tmp_dict))


class Do(object):
    semaphore = threading.BoundedSemaphore(50)
    now_year = time.localtime().tm_year
    now_month = time.localtime().tm_mon
    def __init__(self):
        self.gyas_dict = {}
        # self.gyas = Gongyinansheng(ulType,year, month)

    def run_gyas_once(self,ulType, year, month):
        self.semaphore.acquire()
        gyas = Gongyinansheng(ulType, year, month)
        OneInfo_dict = gyas.getOneInfo()
        if [] not in OneInfo_dict.values():
            self.gyas_dict.update(OneInfo_dict)
        self.semaphore.release()

    def getAllGyas(self):
        t_list = []

        for ulType in [1, 2, 3, 5]:
            # for year in range(2003, self.now_year+1):
            for year in range(self.now_year-1, self.now_year+1):
                for month in range(1,13):
                    t = threading.Thread(target=self.run_gyas_once,args=(ulType,year,month,))
                    t_list.append(t)  # 建立所有线程的list

        # print(len(t_list))
        for t in t_list:
            t.start()  # 批量开始线程
            # time.sleep(0.1)

        for t in t_list:
            t.join()  # 等待所有线程结束，主线程才进行下一步


    def write_data(self):
        with open('..\\db\\getGYAS.txt', 'w') as f:
            f.write(json.dumps(self.gyas_dict))


def getGYAS_run():
    test = Do()
    test.getAllGyas()
    test.write_data()
    print('fine')


# if __name__ == "__main__":
#     getGYAS_run()


'''-----------------------------------------------------------------------'''


# url = r'https://www.icbc-axa.com/axa/getUlPriceByType.do?ulType=1&year=2004&month=1&tb_switch=1'
#
# headers = {
#     'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
#                   r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
#     'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
#     'Connection': 'keep-alive'
# }
# req = request.Request(url, headers=headers)
# page = request.urlopen(req).read()
# page = page.decode('utf-8')
#
# print(type(page))
# print(page)


