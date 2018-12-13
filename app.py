from flask import Flask, render_template, jsonify, request
import data_manipulation
import json

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']


@app.route("/")
def index():
    geojson_centers, geojson_hotels = data_manipulation.get_data(['19.59077506059478', '48.821080079638506'], 2, 50, ['cable_car', 'gondola', 'chair_lift', 'drag_lift', 't-bar', 'j-bar', 'platter', 'rope_tow', 'magic_carpet'], 0, 0)

    return render_template("index.html", ACCESS_KEY=MAPBOX_ACCESS_KEY, geojson=json.dumps(geojson_centers), geojson_hotels=json.dumps(geojson_hotels))


@app.route("/filter", methods=["POST"])
def filter():
    center_range = request.form['center_range']
    hotel_range = request.form['hotel_range']
    snow_range = request.form['snow_range']
    aerialways = request.form.getlist("aerialways")
    red_point_pin_lat = request.form['red_point_pin_lat']
    red_point_pin_lon = request.form['red_point_pin_lon']
    lanovka_range = request.form['lanovka_range']


    geojson_centers, geojson_hotels = data_manipulation.get_data([str(red_point_pin_lat), str(red_point_pin_lon)], hotel_range, center_range, aerialways, snow_range, lanovka_range)
    return json.dumps({'geojson':geojson_centers, 'geojson_hotels': geojson_hotels})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
