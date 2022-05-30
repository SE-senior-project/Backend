import requests
import pandas as pd
from datetime import datetime
from src.config.InitApp import *


def update_external_data(ml, yl):
    # currentMonth = datetime.now().month]
    ml = str(ml)
    yl = str(yl)
    print('month :' + ml)
    print('year :' + yl)
    try:
        cursor = builder.cursor()
        url = 'http://www.indexpr.moc.go.th/PRICE_PRESENT/table_month_regionCsi.asp'
        payload = {
            'DDMonth': ml,
            'DDYear': yl,
            'DDProvince': '50',
            'texttable': 'csi_price_north_web_avg',
            'text_name': 'unit_code_N',
            'B1': '%B5%A1%C5%A7'
        }
        r = requests.post(url, data=payload).content
        df = pd.read_html(r)[0]
        material_price = df[3].to_numpy()
        n = len(material_price) - 1
        sql_update_external_data = '''UPDATE Materials SET material_price = %s  WHERE material_id = %s'''
        for i in range(1, n, 1):
            cursor.execute(sql_update_external_data, (material_price[i], i))
        builder.commit()
        print('Updated external data')
    except:
        print('Update external data fail')

# update_external_data('2', '2565')
