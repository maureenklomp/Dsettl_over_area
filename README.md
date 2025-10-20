# Dsettlement calculations over area
This Viktor tool is meant for calculating the settlement at multiple discrete locations on a site. This allows us to get a feeling for how variable the settlement over an area is over time.

## Input:
- Locations.csv: states the location_ID's, its ground level and its coordinates
- Field_Geological_Descriptions.csv: a list of soil layers, appended for each location, where Description holds the same soil names as in the material input table of the Viktor app.

## Output
- csv with Results for ALL locations: this needs to be downloaded and saved as input for the "Heatmap" and "Restzetting map"

## Current features:
- Cutoff limit for the bottom of the Dsettlement model in m NAP; otherwise overestimating the settlement in the deeper clay- and peat layers.
- Enable vertical drains (including properties for STRIP and COLUMN drains)
- Show soil classification (or borehole data) per location
- Run Dsettlement per location and download
- Run Dsettlement per location and show graph
- Switch between logarithmic and linear axis

## Features to be developed
- Make the unloading time variable for the "restzetting" calculation; now always using 9 months
- Fix the "Results to show on Heatmap" input (and output heatmap)
- Saving and reusing "ALL Settlement Results" instead of the "upload previous results" workaround.
- Optional: Add SANDWALL as option for drains (if needed for a project)
