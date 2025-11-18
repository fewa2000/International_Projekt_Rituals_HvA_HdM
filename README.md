# Rituals Market Analysis – Interactive Geospatial Mapping Project

This project was developed as part of an international collaboration between students from **Stuttgart Media University** and **Amsterdam University of Applied Sciences**, in partnership with **Rituals Cosmetics**. The goal was to build an **interactive geospatial map** visualizing Rituals’ store presence across Europe, comparing it with a major competitor, and overlaying key socioeconomic indicators.

---

## Overview

The resulting map provides a combined view of store locations and regional characteristics, supporting market insights and strategic expansion analysis.

**Map features:**
- Rituals store locations  
- Competitor store locations  
- NUTS 3 regional boundaries  
- Socioeconomic overlays (population density & GDP)  
- Fully interactive map built using Python and Folium  
- Optimized vector tiles for fast loading on mobile and desktop

---

## Key Features

- **Interactive Map**
  - Separate markers for Rituals and competitor stores
  - Interactive tooltips and visual overlays

- **NUTS 3 Regional Data Integration**
  - Population density
  - Regional GDP values

- **Vector Tile Optimization**
  - Vector tiles generated with **Tippecanoe**
  - Served locally using **tileserver-gl**
  - Ensures mobile-friendly performance and smooth loading

- **Custom TileLayers in Folium**
  - Integrated vector tiles through a custom Folium configuration
  - Reduced map size without losing essential detail

---

## Technical Approach

### 1. Geospatial Data Preparation
- Worked with **SHP files**, CSV store datasets, and NUTS 3 metadata  
- Cleaned, transformed, and aligned regional and coordinate data  
- Linked store locations to their corresponding NUTS 3 regions  

### 2. Vector Tile Generation & Hosting
- Set up an **Ubuntu shell environment** on a local machine  
- Generated MBTiles using **Tippecanoe**  
- Hosted tiles locally with **tileserver-gl** for quick map rendering  

### 3. Map Development in Python
- Built the map using **Folium**
- Added store markers with distinguishable icons  
- Integrated vector tiles via Folium’s `TileLayer`  
- Ensured responsiveness and browser compatibility  

---

## Collaboration

This was a highly coordinated international team project.  
Roles were clearly defined, communication was strong, and collaboration was smooth throughout.

Our project was **selected by Rituals as the most convincing final product**, reflecting both technical execution and clear analytical value.
