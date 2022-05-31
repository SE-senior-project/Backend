from src.config.Service import *
import pandas as pd


def generate_project(contractor_id):
    cursor = builder.cursor()
    array_project = []
    output = []
    prepare_output = []
    tran_tuple = ""
    sql_generate_project = '''
           SELECT *
           FROM Projects
           WHERE Projects.contractor_id = %s
       '''
    cursor.execute(sql_generate_project, (1,))
    result = cursor.fetchall()
    df = pd.DataFrame(result)

