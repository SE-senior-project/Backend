import requests
from bs4 import BeautifulSoup
import pandas as pd

ml = '03'
yl = '2565'
pl = '50'

url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
payload = {
    'DDMonth': ml,
    'DDYear': yl,
    'DDProvince': pl,
    'texttable': 'csi_price_north_web_avg',
    'text_name': 'unit_code_N',
    'B1': '%B5%A1%C5%A7'
}
r = requests.post(url, data=payload).content
soup = BeautifulSoup(r, 'html.parser')
df = pd.read_html(r)[0]
material_name = df[1].to_numpy()
material_type = df[2].to_numpy()
material_price = df[3].to_numpy()
