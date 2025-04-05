from arcgis import GIS
from arcgis.features import FeatureLayerCollection
import requests
from datetime import datetime
from ipywidgets import * 
from arcgis.features.analysis import interpolate_points



# API URLs for Weather and Air Quality
weather_urls = [
    "https://api.openweathermap.org/data/2.5/weather?lat=5.4636898&lon=-74.6501244&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.755758850999623&lon=-74.62678180957127&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.471854056255329&lon=-74.59601949154832&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.7465651257591865&lon=-74.51680756910774&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.629145047931948&lon=-74.58252185001554&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5,6618&lon=-74,5264&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.5707564524864175&lon=-74.61515311188553&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.679725712726425&lon=-74.61971546924745&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.778461317941011&lon=-74.69841613285665&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/weather?lat=5.610487194080601&lon=-74.51021889167716&appid=4b8fc198ba3b9d196c707d6f663b274e"
    
]

air_quality_urls = [
    "https://api.openweathermap.org/data/2.5/air_pollution?lat=5.4636898&lon=-74.6501244&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/air_pollution?lat=5.755758850999623&lon=-74.62678180957127&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/air_pollution?lat=5.471854056255329&lon=-74.59601949154832&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/air_pollution?lat=5.7465651257591865&lon=-74.51680756910774&appid=4b8fc198ba3b9d196c707d6f663b274e",
    "https://api.openweathermap.org/data/2.5/air_pollution?lat=5.629145047931948&lon=-74.58252185001554&appid=4b8fc198ba3b9d196c707d6f663b274e"
]

# Layer schemas
weather_service_name = "OpenWeatherService"
weather_schema = {
    "fields": [
        {"name": "OBJECTID", "type": "esriFieldTypeOID", "alias": "OBJECTID"},
        {"name": "RecordID", "type": "esriFieldTypeInteger", "alias": "Record ID"},
        {"name": "RecordTime", "type": "esriFieldTypeDate", "alias": "Record Time"},
        {"name": "City", "type": "esriFieldTypeString", "alias": "City", "length": 255},
        {"name": "Latitude", "type": "esriFieldTypeDouble", "alias": "Latitude"},
        {"name": "Longitude", "type": "esriFieldTypeDouble", "alias": "Longitude"},
        {"name": "Temperature", "type": "esriFieldTypeDouble", "alias": "Temperature (°C)"},
        {"name": "TempMin", "type": "esriFieldTypeDouble", "alias": "Min Temperature (°C)"},
        {"name": "TempMax", "type": "esriFieldTypeDouble", "alias": "Max Temperature (°C)"},
        {"name": "Humidity", "type": "esriFieldTypeDouble", "alias": "Humidity (%)"},
        {"name": "Weather", "type": "esriFieldTypeString", "alias": "Weather Description", "length": 255},
        {"name": "WindSpeed", "type": "esriFieldTypeDouble", "alias": "Wind Speed (m/s)"}
    ],
    "geometryType": "esriGeometryPoint",
    "spatialReference": {"wkid": 4326},
    "name": "Weather Data"
}

air_quality_service_name = "AirQualityService"
air_quality_schema = {
    "fields": [
        {"name": "OBJECTID", "type": "esriFieldTypeOID", "alias": "OBJECTID"},
        {"name": "RecordID", "type": "esriFieldTypeInteger", "alias": "Record ID"},
        {"name": "RecordTime", "type": "esriFieldTypeDate", "alias": "Record Time"},
        {"name": "City", "type": "esriFieldTypeString", "alias": "City", "length": 255},
        {"name": "Latitude", "type": "esriFieldTypeDouble", "alias": "Latitude"},
        {"name": "Longitude", "type": "esriFieldTypeDouble", "alias": "Longitude"},
        {"name": "AQI", "type": "esriFieldTypeInteger", "alias": "Air Quality Index"},
        {"name": "PM10", "type": "esriFieldTypeDouble", "alias": "PM10"},
        {"name": "PM25", "type": "esriFieldTypeDouble", "alias": "PM2.5"},
        {"name": "CO", "type": "esriFieldTypeDouble", "alias": "Carbon Monoxide (CO)"},
        {"name": "NO2", "type": "esriFieldTypeDouble", "alias": "Nitrogen Dioxide (NO2)"},
        {"name": "SO2", "type": "esriFieldTypeDouble", "alias": "Sulfur Dioxide (SO2)"},
        {"name": "O3", "type": "esriFieldTypeDouble", "alias": "Ozone (O3)"}
    ],
    "geometryType": "esriGeometryPoint",
    "spatialReference": {"wkid": 4326},
    "name": "Air Quality Data"
}

# Function to create feature layer
def create_feature_layer(service_name, schema, description):
    existing_service = None
    for item in gis.content.search(query=f"title:{service_name}", item_type="Feature Service"):
        if item.title == service_name:
            existing_service = item
            break

    if not existing_service:
        service = gis.content.create_service(
            name=service_name,
            service_description=description,
            has_static_data=False,
            max_record_count=1000,
            supported_query_formats="JSON",
            capabilities="Query,Editing,Create,Update,Delete",
            wkid=4326,
            tags=["OpenWeather", "Climate"],
            snippet=description
        )
    else:
        service = existing_service

    flc = FeatureLayerCollection.fromitem(service)
    if not flc.layers:
        flc.manager.add_to_definition({"layers": [schema]})
    return flc

# Function to populate data
def populate_layer(urls, flc, is_air_quality=False):
    layer = flc.layers[0]
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            record_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            unique_id = int(datetime.now().timestamp())
            features = []

            if is_air_quality:
                aqi_data = data["list"][0]
                features.append({
                    "geometry": {"x": data["coord"]["lon"], "y": data["coord"]["lat"]},
                    "attributes": {
                        "RecordID": unique_id,
                        "RecordTime": record_time,
                        "City": "Station",
                        "Latitude": data["coord"]["lat"],
                        "Longitude": data["coord"]["lon"],
                        "AQI": aqi_data["main"]["aqi"],
                        "PM10": aqi_data["components"]["pm10"],
                        "PM25": aqi_data["components"]["pm2_5"],
                        "CO": aqi_data["components"]["co"],
                        "NO2": aqi_data["components"]["no2"],
                        "SO2": aqi_data["components"]["so2"],
                        "O3": aqi_data["components"]["o3"]
                    }
                })
            else:
                features.append({
                    "geometry": {"x": data["coord"]["lon"], "y": data["coord"]["lat"]},
                    "attributes": {
                        "RecordID": unique_id,
                        "RecordTime": record_time,
                        "City": data["name"],
                        "Latitude": data["coord"]["lat"],
                        "Longitude": data["coord"]["lon"],
                        "Temperature": data["main"]["temp"] - 273.15,
                        "TempMin": data["main"]["temp_min"] - 273.15,
                        "TempMax": data["main"]["temp_max"] - 273.15,
                        "Humidity": data["main"]["humidity"],
                        "Weather": data["weather"][0]["description"],
                        "WindSpeed": data["wind"]["speed"]
                    }
                })

            layer.edit_features(adds=features)

# Create weather layer
weather_flc = create_feature_layer(weather_service_name, weather_schema, "Weather Data Layer")
populate_layer(weather_urls, weather_flc, is_air_quality=False)

# Create air quality layer
air_quality_flc = create_feature_layer(air_quality_service_name, air_quality_schema, "Air Quality Data Layer")
populate_layer(air_quality_urls, air_quality_flc, is_air_quality=True)

# Create view for air quality layer
view_name = "AirQualityView"
existing_view = None
for item in gis.content.search(query=f"title:{view_name}", item_type="Feature Service"):
    if item.title == view_name:
        existing_view = item
        break

if not existing_view:
    air_quality_view = air_quality_flc.manager.create_view(name=view_name)
else:
    air_quality_view = FeatureLayerCollection.fromitem(existing_view)

print("Data and view setup completed.")
