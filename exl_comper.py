import xlrd
import xlwt
from aip import AipNlp

APP_ID = '11801619'
API_KEY = 'G37OerKlmaUWrFwizpCvfONf'
SECRET_KEY = 'w0URILF7WV9kiddK7dYxGPDFKKv4BvFs'

nlp_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

workbook = xlrd.open_workbook(r'file/test.xlsx')
sheet = workbook.sheet_by_index(0)
row = sheet.nrows
line = sheet.ncols

text1 = sheet.col(0)
text2 = sheet.col(1)


# print(text1)
# print('-------------------')
# print(text2)


# for i in text1:
#     print(i.value)
#
# for i in text2:
#     print(i.value)


def text_one(args):
    for i in args:
        res = i.value
    return res


def text_two(args):
    for j in args:
        res = j.value
    return res


print(text_one(text1))
# if not nlp_client.simnet(text_one(text1), text_two(text2)).get("score") >= 0.9:
# if not text_one(text1) == text_two(text2):
#     print(text_one(text1), text_two(text2))
