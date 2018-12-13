import pandas as pd
import psycopg2

def load_data(path='static/datasets/centrums_with_coords_new.csv'):
    df = pd.read_csv(path)
    return df


def df_to_geojson(df, properties):
    geojson = {'type':'FeatureCollection', 'features':[]}

    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'geometry':{'type':'Point',
                               'coordinates':[]},
                    'properties':{}}
        feature['geometry']['coordinates'] = [row['lon'],row['lat']]
        for property in properties:
            feature['properties'][property] = row[property]
        geojson['features'].append(feature)

    return geojson


def get_data(user_coords, radius_hotel, radius_ski_center, type_of_aerialways, snow, lanovka_range):
    conn = psycopg2.connect(dbname='PDT_ski', port='5432', user='postgres', password='', host='localhost')
    curs = conn.cursor()


    sql_ski_centers = "SELECT ski_center_name, lon, lat, snow, sum(aerialway_length) as aerialways_length FROM centers_with_aerialways WHERE ST_DWithin( ski_center_geom::geography, ST_SetSRID( ST_MakePoint(%s,%s), 4326)::geography, %s * 1000 ) AND aerialway_tags->'aerialway'IN %s AND snow >= %s GROUP BY ski_center_name, lon, lat, snow HAVING sum(aerialway_length) >= %s;"
    curs.execute(sql_ski_centers,(user_coords[0],user_coords[1], radius_ski_center, tuple(type_of_aerialways), snow, lanovka_range))
    ski_centers = curs.fetchall()
    ski_centers_df =  pd.DataFrame(ski_centers, columns=['name', 'lon', 'lat', 'snow', 'aerialways_length'])
    ski_centers_geojson = df_to_geojson(ski_centers_df, ['name', 'snow', 'aerialways_length'])


    sql_hotels= """WITH ski_centers_in_radius AS (
                    SELECT ski_center_name, ski_center_geom FROM centers_with_aerialways
                    WHERE ST_DWithin( ski_center_geom::geography, ST_SetSRID( ST_MakePoint(%s,%s), 4326)::geography, %s * 1000 )
                    AND aerialway_tags->'aerialway'IN %s AND snow >= %s GROUP BY ski_center_name, snow, ski_center_geom HAVING sum(aerialway_length) >= %s)
                    SELECT DISTINCT ON(hotels.name) hotels.name, hotels.lon , hotels.lat FROM hotels INNER JOIN ski_centers_in_radius
                    ON ST_DWithin(ski_centers_in_radius.ski_center_geom, hotels.way, %s)"""
    curs.execute(sql_hotels,(user_coords[0],user_coords[1], radius_ski_center, tuple(type_of_aerialways), snow, lanovka_range, str(float(radius_hotel)*0.01)))
    hotels = curs.fetchall()
    hotels_df =  pd.DataFrame(hotels, columns=['name', 'lon', 'lat'])
    hotels_geojson = df_to_geojson(hotels_df, ['name'])

    return ski_centers_geojson, hotels_geojson
