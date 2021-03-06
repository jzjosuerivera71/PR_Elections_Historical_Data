import numpy as np
import pandas as pd
import urllib.request
import re
from bs4 import BeautifulSoup


def get_data(year, position):
    if position == 'gobernador':
        position = 'g'
    elif position == 'comisionado_residente':
        position = 'c'
    elif position == 'alcalde':
        position = 'a'
        
    response = urllib.request.urlopen('http://209.68.12.238/cgi-bin/eventos.pl?evento=' + 
                                      year + '&voto=' + position)
    webpage = response.read()
    soup = BeautifulSoup(webpage, 'html.parser')
    
    return soup
    
def get_rows(soup):
    table = soup.find_all('table')[5]
    table_rows = table.find_all('tr')
    tr = table_rows[0]
    td = tr.find_all('td')
    row = [tr.text for tr in td]
    
    return row

def get_columns(soup):
    table = soup.find_all('table')[5]
    column_values = table.find_all('th')
    cols = [th.text for th in column_values]
    cols = cols[1:((len(cols)//2) - 1)]
    new_colnames = ['municipios']
    
    for values in cols:
        if values == 'Total':
            break
        
        try:
            split_value = values.split('(')[1].replace(')', '')
        except:
            split_value = values
        parsed_value = '_'.join(re.findall('[A-Z][^A-Z]*', split_value))
        new_colnames.append('votos_' + parsed_value)
        new_colnames.append('pct_' + parsed_value)
    
    new_colnames += ['total']
    return new_colnames
    
def save_csv(rows, shape, column_names, year, position):
    np_year = np.array(rows)
    np_year.shape = shape
    
    df = pd.DataFrame(np_year, columns = column_names)
    df.to_csv('../../data/temporary_data/' + position +
                 '/data_' + year + '.csv' )
    
def execute_pipeline(year, position, shape):
    data = get_data(year, position)
    rows_data = get_rows(data)
    columns = get_columns(data)
    save_csv(rows_data, shape, columns, year, position)
    
def execute_pipeline_alcaldia(year, position, shape):
    data = get_data(year, position)
    rows_data = get_rows(data)
    columns = get_columns_alcaldias(data)
    save_csv(rows_data, shape, columns, year, position)
                
execute_pipeline('1932', 'comisionado_residente', (78, 14))
execute_pipeline('1936', 'comisionado_residente', (78, 10))
execute_pipeline('1940', 'comisionado_residente', (78, 16))
execute_pipeline('1944', 'comisionado_residente', (78, 16))

execute_pipeline('1980', 'comisionado_residente', (79, 8))
execute_pipeline('1984', 'comisionado_residente', (80, 10))
execute_pipeline('1988', 'comisionado_residente', (80, 8))
execute_pipeline('1992', 'comisionado_residente', (79, 10))
execute_pipeline('1996', 'comisionado_residente', (79, 14)) 
execute_pipeline('2000', 'comisionado_residente', (79, 14))

execute_pipeline('1948', 'gobernador', (78, 14))
execute_pipeline('1952', 'gobernador', (77, 10))
execute_pipeline('1956', 'gobernador', (78, 8))
execute_pipeline('1960', 'gobernador', (77, 10))
execute_pipeline('1964', 'gobernador', (77, 10))
execute_pipeline('1968', 'gobernador', (77, 12))
execute_pipeline('1972', 'gobernador', (79, 14))
execute_pipeline('1976', 'gobernador', (79, 10))
execute_pipeline('1980', 'gobernador', (79, 10))
execute_pipeline('1984', 'gobernador', (79, 10))
execute_pipeline('1988', 'gobernador', (79, 8))
execute_pipeline('1992', 'gobernador', (79, 10))
execute_pipeline('1996', 'gobernador', (79, 14))
execute_pipeline('2000', 'gobernador', (79, 14))

execute_pipeline('1976', 'alcalde', (79, 14))
execute_pipeline('1980', 'alcalde', (79, 14))
execute_pipeline('1984', 'alcalde', (79, 12))
# execute_pipeline('1988', 'alcalde', (79, 14)) # No-Data
execute_pipeline('1992', 'alcalde', (79, 14))
execute_pipeline('1996', 'alcalde', (79, 18))
execute_pipeline('2000', 'alcalde', (79, 18))
