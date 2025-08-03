import geopandas as gpd
from shapely.geometry import Point

def islocationwithincountry(lat, lon):
    # Path to the downloaded and extracted shapefile
    shapefile_path = "data/ne_110m_admin_0_countries.shp"

    # Load the shapefile
    world = gpd.read_file(shapefile_path)

    point = Point(lon, lat)

    # Select the row(s) where the polygon contains the point
    country = world[world.contains(point)]

    if not country.empty:
        # Compare the NAME column to the expected country name
        #return country.iloc[0]['NAME'] == country_selected, country.iloc[0]['NAME'] 
        print (f"Country found: {country.iloc[0]['NAME']}")
        return True, country.iloc[0]['NAME']
    else:
        return False, None

def getdistancetoborderinfo(lat, lon, country):
    rounding_digits = 1

    # Path to the downloaded and extracted shapefile
    shapefile_path = "data/ne_110m_admin_0_countries.shp"

    # Load the shapefile
    world = gpd.read_file(shapefile_path)
    # Reproject to World Mercator (EPSG:3395) for greater accuracy
    world = world.to_crs(epsg=3395)

    location = Point(lon, lat)
    # Reproject point to the same CRS for accuracy
    location_gdf = gpd.GeoSeries([location], crs="EPSG:4326").to_crs(epsg=3395)
    projected_point = location_gdf.iloc[0]

    # Get the country geometry
    target_country = world[world['NAME'] == country]

    if target_country.empty:
        return None, None, None, None
    
    # Distance in meters
    distance_to_border_meters = projected_point.distance(target_country.geometry.iloc[0].boundary)
    #Distance in miles
    distance_to_border_miles = round(distance_to_border_meters / 1609.344, rounding_digits)
    #Distance in kilometers
    distance_to_border_km = round(distance_to_border_meters / 1000, rounding_digits)
    
    # Get closest border point
    boundary = target_country.geometry.iloc[0].boundary
    closest_point = boundary.interpolate(boundary.project(projected_point))
    # Convert back to lat/lon
    closest_point_latlon = gpd.GeoSeries([closest_point], crs=world.crs).to_crs(epsg=4326).iloc[0]
    closest_lat = closest_point_latlon.y
    closest_lon = closest_point_latlon.x

    # Return distance_to_border_miles, distance_to_border_km, closest_lat, closest_lon
    return distance_to_border_miles, distance_to_border_km, closest_lat, closest_lon