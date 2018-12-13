import psycopg2
import pandas as pd
from random import randint

conn = psycopg2.connect(dbname='PDT_ski', port='5432', user='postgres', password='', host='localhost')
sql = "UPDATE shmu_ski SET snow=%s WHERE name=%s"

ski_centers = pd.read_csv('strediska.csv', header=None)

for _, row in ski_centers.iterrows():
	with conn.cursor() as cur:
		cur.execute(sql, (row[1].split()[0], row[0]))

conn.commit()
conn.close()
