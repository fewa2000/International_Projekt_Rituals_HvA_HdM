import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from shapely.geometry import Point
import folium

# 1. Load the Rituals store data
df = pd.read_csv(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\FINAL_all_rituals_locations_with_kpis.csv', delimiter=';', encoding='ISO-8859-1')

# Initialize geolocator with retries to avoid timeout issues
geolocator = Nominatim(user_agent="rituals_geocoder", timeout=5)

# Create empty lists to store latitude and longitude
latitudes = []
longitudes = []

# Geocode each address in the CSV file
for idx, row in df.iterrows():
    try:
        location = geolocator.geocode(f"{row['Address']}, {row['City']}, {row['Country']}")
        if location:
            latitudes.append(location.latitude)
            longitudes.append(location.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
    except:
        latitudes.append(None)
        longitudes.append(None)

# Add the lat/lon data to the DataFrame
df['Latitude'] = latitudes
df['Longitude'] = longitudes

# Remove rows where geocoding failed
df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# Convert the DataFrame into a GeoDataFrame
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
geo_df = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# 1.1 Load the Aveda store data
df_aveda = pd.read_csv(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\FINAL_Aveda_NL_DE.csv', delimiter=';', encoding='ISO-8859-1')

# Initialize geolocator for Aveda
geolocator_aveda = Nominatim(user_agent="aveda_geocoder", timeout=5)

# Create empty lists to store latitude and longitude for Aveda
latitudes_aveda = []
longitudes_aveda = []

# Geocode each address in the Aveda CSV file
for idx, row in df_aveda.iterrows():
    try:
        location = geolocator_aveda.geocode(f"{row['Address']}, {row['City']}")
        if location:
            latitudes_aveda.append(location.latitude)
            longitudes_aveda.append(location.longitude)
        else:
            latitudes_aveda.append(None)
            longitudes_aveda.append(None)
    except:
        latitudes_aveda.append(None)
        longitudes_aveda.append(None)

# Add the lat/lon data to the Aveda DataFrame
df_aveda['Latitude'] = latitudes_aveda
df_aveda['Longitude'] = longitudes_aveda

# Remove rows where geocoding failed
df_aveda.dropna(subset=['Latitude', 'Longitude'], inplace=True)

# Convert the Aveda DataFrame into a GeoDataFrame
geometry_aveda = [Point(xy) for xy in zip(df_aveda['Longitude'], df_aveda['Latitude'])]
geo_df_aveda = gpd.GeoDataFrame(df_aveda, geometry=geometry_aveda, crs="EPSG:4326")


# 2. Load the NUTS 3 shapefiles
nuts3_shapefile = gpd.read_file(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\NUTS_RG_20M_2021_3035.shp\NUTS_RG_20M_2021_3035.shp', encoding='ISO-8859-1')

# Ensure the CRS is correct for both GeoDataFrames
if nuts3_shapefile.crs != "EPSG:4326":
    nuts3_shapefile = nuts3_shapefile.to_crs("EPSG:4326")

# 3. Load the Eurostat data (Population structure indicators by NUTS 3 region)
eurostat_data = pd.read_csv(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\FINAL_nut3_population_2019.csv', delimiter=',', encoding='ISO-8859-1')

# Clean the column names and replace missing values
eurostat_data.columns = eurostat_data.columns.str.strip()
eurostat_data.replace(':', None, inplace=True)

# Select relevant data and drop missing values
eurostat_2019 = eurostat_data[['geo', '2019']].dropna()

# Convert '2019' to numeric
eurostat_2019['2019'] = pd.to_numeric(eurostat_2019['2019'], errors='coerce')

# 4. Merge NUTS 3 shapefile with Eurostat data based on NUTS 3 region codes (geo)
merged_gdf = nuts3_shapefile.merge(eurostat_2019, left_on='NUTS_ID', right_on='geo')

# 5. Create a Folium map centered in Europe
m = folium.Map(location=[50, 10], zoom_start=4)

# 6. Add vector tiles (replace {server_url} with the local or hosted URL)
folium.TileLayer(
    tiles='http://localhost:8080/data/{z}/{x}/{y}.pbf',  
    attr='Map data',
    name='Vector Tiles',
    overlay=True,
    control=True
).add_to(m)

# Add choropleth for population structure data (from Eurostat, colored by the '2019' column)
folium.Choropleth(
    geo_data=merged_gdf,
    name='choropleth',
    data=merged_gdf,
    columns=['NUTS_ID', '2019'],  # NUTS 3 ID and 2019 population data
    key_on='feature.properties.NUTS_ID',
    fill_color='YlGnBu',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population Structure (2019)',
    nan_fill_color='white'  # Set color for regions with missing population data
).add_to(m)

# 7. Add popups or tooltips for each region
for idx, row in merged_gdf.iterrows():
    folium.GeoJson(
        row['geometry'],
        tooltip=folium.Tooltip(f"Region: {row['NUTS_ID']}<br>Population: {row['2019']}"),
        popup=folium.Popup(f"Region: {row['NUTS_ID']}<br>Population: {row['2019']}"),
        style_function=lambda x: {
            'fillColor': 'transparent',  # Keep fill transparent to avoid overlapping with vector tiles
            'color': 'black',  # Border color for the regions
            'weight': 1,  # Border weight
            'fillOpacity': 0  # Ensure the region is clickable without color overlay
        }
    ).add_to(m)

# 8. Add markers for each Rituals store location
for idx, row in geo_df.iterrows():
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=f"{row['Name']}<br>{row['Address']}<br>ATV: {row['ATV']}<br>Customer: {row['Customer']}",
        icon=folium.Icon(color='blue')  # Blue markers for Rituals stores
    ).add_to(m)

# 8.1 Add Aveda store markers
for idx, row in geo_df_aveda.iterrows():
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=f"{row['Name']}<br>{row['Address']}",
        icon=folium.Icon(color='green')  # Green markers for Aveda stores
    ).add_to(m)

# 9. Save the map to an HTML file
m.save("FINAL_rituals_avenda_store_map_with_vector_tiles_population_FULL_MAP.html")

