import json
import xlwt
import time
import sys
import os


# Base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0,Base_path)


# '''["5","2005-01-04","  0.0000","  0.0000","2005","0","0"]'''

class ExcelGYAS(object):
    now_year = time.localtime().tm_year
    now_month = time.localtime().tm_mon
    def __init__(self,f):
        self.gyas_dict = json.loads(f.read())
        self.wb = xlwt.Workbook()
        self.ws1 = self.wb.add_sheet('卓越',cell_overwrite_ok=True)
        self.ws2 = self.wb.add_sheet('稳健',cell_overwrite_ok=True)
        self.ws3 = self.wb.add_sheet('安心',cell_overwrite_ok=True)
        self.ws4 = self.wb.add_sheet('进取',cell_overwrite_ok=True)

    def writeexcel(self,path):
        for ulType, ws in [(1, self.ws1), (2, self.ws2), (3, self.ws3), (5, self.ws4)]:
            ws.write(0, 0, "日期")
            ws.write(0, 1, "买入价")
            ws.write(0, 2, "卖出价")
            n = 1
            for year in range(2003, self.now_year+1):
                for month in range(1, 13):
                    s_key = '{}_{}_{}'.format(ulType, year, month)
                    if s_key in self.gyas_dict:
                        key_list = self.gyas_dict[s_key]
                        for idx, value in enumerate(key_list):
                            if "  0.0000" in value:
                                continue
                            ws.write(n, 0, value[1].replace('-','/'))
                            ws.write(n, 1, value[2].replace('-','/'))
                            ws.write(n, 2, value[3].replace('-','/'))
                            n += 1

        self.wb.save(path)


def ExcelGYAS_run():
    with open('..\\db\\getGYAS.txt','r') as f:
        GYAS = ExcelGYAS(f)
        # GYAS.writeexcel("{}\\bin\\工银安盛账户.xls".format(Base_path))
        GYAS.writeexcel("..\\bin\\工银安盛账户.xls")

# if __name__ == "__main__":
#     ExcelGYAS_run()