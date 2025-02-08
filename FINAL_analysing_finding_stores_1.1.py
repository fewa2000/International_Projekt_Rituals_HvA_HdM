import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from shapely.geometry import Point
import folium
import time
import random

# Load the Rituals store data
df = pd.read_csv(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\FINAL_all_rituals_locations_with_kpis.csv', delimiter=';', encoding='ISO-8859-1')

# Initialize geolocator with a longer timeout
geolocator = Nominatim(user_agent="rituals_geocoder", timeout=5)

# Function to geocode with retries
def geocode_with_retry(address, max_retries=3):
    for attempt in range(max_retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                print(f"Address not found: {address}")
                return None, None
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            if attempt < max_retries - 1:
                print(f"Geocoding attempt {attempt + 1} failed for {address}. Retrying...")
                time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds
            else:
                print(f"Max retries reached for {address}. Error: {e}")
                return None, None

# Lists to store successfully geocoded and failed addresses
geocoded_data = []
failed_data = []

# Geocode each address in the CSV file
for idx, row in df.iterrows():
    address = f"{row['Address']}, {row['City']}, {row['Country']}"
    lat, lon = geocode_with_retry(address)
    
    if lat is not None and lon is not None:
        geocoded_data.append({
            'Name': row['Name'],
            'Address': row['Address'],
            'City': row['City'],
            'Country': row['Country'],
            'Latitude': lat,
            'Longitude': lon
        })
    else:
        print(f"Skipping address: {address}")
        failed_data.append({
            'Name': row['Name'],
            'Address': row['Address'],
            'City': row['City'],
            'Country': row['Country']
        })
    
    time.sleep(random.uniform(1, 2))  # Random delay between requests to avoid rate limiting

# Create a DataFrame with successfully geocoded addresses
geocoded_df = pd.DataFrame(geocoded_data)

# Create a DataFrame with failed geocoded addresses
failed_df = pd.DataFrame(failed_data)

# Save successfully geocoded addresses to a CSV file
geocoded_df.to_csv(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\FINAL_successfully_geocoded.csv', index=False)

# Save failed geocoded addresses to a CSV file
failed_df.to_csv(r'C:\Users\wald_\OneDrive\Dokumente\Hochschule der Medien\International_Projekt_Rituals_HvA_HdM\FINAL_failed_geocoded.csv', index=False)

# Convert the successfully geocoded DataFrame into a GeoDataFrame
geometry = [Point(xy) for xy in zip(geocoded_df['Longitude'], geocoded_df['Latitude'])]
geo_df = gpd.GeoDataFrame(geocoded_df, geometry=geometry, crs="EPSG:4326")

# Print summary of geocoding results
print(f"Total addresses: {len(df)}")
print(f"Successfully geocoded: {len(geocoded_df)}")
print(f"Failed to geocode: {len(df) - len(geocoded_df)}")
