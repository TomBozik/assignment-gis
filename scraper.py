import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = 'http://www.shmu.sk/sk/?page=68'
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

tables = soup.findChildren('table')
resorts_table = tables[0]
rows = resorts_table.findChildren(['th', 'tr'])

file = open('strediska.csv', 'w')

for row in rows[1:]:
    cells = row.findChildren('td')
    for i, cell in enumerate(cells):
        if (i == 0) or (i ==2):
            file.write(cell.string+",")
        if i == 3:
            file.write(cell.string)
    file.write("\n")

file.close()
