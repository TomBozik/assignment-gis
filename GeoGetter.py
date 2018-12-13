# locationiq.com
# FREE:
# 10,000 requests /day
# 60 requests /minute
# 2 requests /second
# street maps only

import pandas as pd
import urllib.request, urllib.parse
import json
import operator
from time import sleep

API_KEY='d8bd2042ba4740'
COUNTRY='sk'

coordinates = list()
snow_data = pd.read_csv('strediska.csv', header=None)
ski_centrums= snow_data[snow_data.columns[0]].tolist()

for centrum in ski_centrums:
    try:
        contents = urllib.request.urlopen("https://us1.locationiq.com/v1/search.php?key="+API_KEY+"&q="+urllib.parse.quote(centrum)+"&format=json&countrycodes="+COUNTRY).read()
        json_data = json.loads(contents)[0]
        coordinates.append((json_data['lat'], json_data['lon']))
        sleep(1)
    except Exception:
        coordinates.append(('0', '0'))

lat = list(map(operator.itemgetter(0), coordinates))
lon = list(map(operator.itemgetter(1), coordinates))

centrums_with_coords = pd.DataFrame(
    {'name': ski_centrums,
     'lat': lat,
     'lon': lon
    })
    
centrums_with_coords.to_csv('centrums_with_coords.csv', index=False)
