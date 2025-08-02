from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from geolocate import isvalidcountry, islocationwithincountry, getdistancetoborderinfo

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/favicon.ico")
def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/apple-touch-icon.png")
def apple_icon():
    return FileResponse("static/apple-touch-icon.png")

@app.get("/")
def read_root():
    msg = "Welcome to the Border Proximity API. Use /getborderproximity to get distance to border information."
    return {"message": msg}

#API endpoint format
#http://127.0.0.1:8000/getborderproximity?latitude=32.78&longitude=-96.80&country=United%20States%20of%20America
@app.get("/getborderproximity")
def add(latitude: float, longitude: float, country: str):
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return {"error": "Invalid latitude or longitude value."}
    if not isinstance(country, str) or not isvalidcountry(country):
        return {"error": "Invalid country name."}
    
    # Check to see if location is within the country
    if not islocationwithincountry(latitude, longitude, country):
        if country == "United States of America":
            return {"notincountry": "The specified location is not within the United States border."}
        else:
            return {"notincountry": "The specified location is not within " + country + "border."}

    # Border proximity calculation logic
    result = getdistancetoborderinfo(latitude, longitude, country)

    # If the result is None, it means the country was not found
    if result is None:
        return {"error": "Country not found."}
    else:
        # Result array = distance_to_border_miles, distance_to_border_km, closest_lat, closest_lon
        if result[0] is not None:
            # Create a Google Maps path link for the closest border point
            path_link = "https://www.google.com/maps/dir/{},{}/{},{}".format(latitude, longitude, round(result[2],3), round(result[3],3))
            return {
                "distance_miles": result[0],
                "distance_km": result[1],
                "map_path_link": path_link
            }
        else:
            return {"error": "Could not calculate distance to border."}
            