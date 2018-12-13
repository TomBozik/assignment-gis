import psycopg2
import pandas as pd

conn = psycopg2.connect(dbname='PDT_ski', port='5432', user='postgres', password='', host='localhost')
sql = "INSERT INTO shmu_ski (name, lon, lat, geom) VALUES (%s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))"

ski_centers = pd.read_csv('centrums_with_coords_new.csv')

for _, row in ski_centers.iterrows():
	with conn.cursor() as cur:
		cur.execute(sql, (row['name'], row['lon'], row['lat'], row['lon'], row['lat']))
conn.commit()
