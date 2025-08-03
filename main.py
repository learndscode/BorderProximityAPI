from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from geolocate import islocationwithincountry, getdistancetoborderinfo

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
#http://127.0.0.1:8000/getborderproximity?latitude=32.78&longitude=-96.80   // Dallas, TX
#http://127.0.0.1:8000/getborderproximity?latitude=28.925&longitude=34.113  // Egypt
#http://127.0.0.1:8000/getborderproximity?latitude=28.925&longitude=34.113  // Atlantic Ocean

#https://borderproximityapi.onrender.com/getborderproximity?latitude=32.78&longitude=-96.80
#https://borderproximityapi.onrender.com/getborderproximity?latitude=28.925&longitude=34.113 // Egyp
#https://borderproximityapi.onrender.com/getborderproximity?latitude=20.0&longitude=-40.0

@app.get("/getborderproximity")
def add(latitude: float, longitude: float):
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return {"error": "Invalid latitude or longitude value."}
   
    countyresult = islocationwithincountry(latitude, longitude)

    if not countyresult[0]:
        return {"notincountry": "Could not determine the country for the specified coordinates."}
    
    # Border proximity calculation logic
    result = getdistancetoborderinfo(latitude, longitude, countyresult[1])

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
                "locatedcountry": countyresult[1],
                "map_path_link": path_link
            }
        else:
            return {"error": "Could not calculate distance to border."}
            