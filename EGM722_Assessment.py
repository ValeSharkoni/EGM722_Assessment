
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap



# Replace the file path to 'attacks.csv' with the path to where the CSV file is saved.
# I loaded the repository manually, by saving the CSV file within my assessment folder
file_path = 'attacks.csv'

# Load the CSV file
data = pd.read_csv(file_path)


# Display the first few rows of the dataframe to check it was loaded correctly
print(data.head())

# Despite having done extensive cleaning manually,
# there are still some problems: strip whitespace from the column names
data.columns = data.columns.str.strip()
# Standardize the species names to ensure consistency
data['Species'] = data['Species'].str.strip().str.lower().str.title()
# Clean the 'Fatal (Y/N)' column
data['Fatal (Y/N)'] = data['Fatal (Y/N)'].str.strip().str.upper()
# Filter out any rows where 'Fatal (Y/N)' is not 'Y' or 'N' since there are some NA
data = data[data['Fatal (Y/N)'].isin(['Y', 'N'])]

#with the following code, we can investigate some patterns in the data
#and ask questions like 1) how many attacks have been reported each year since 1960
#2) how many attacks have been recorded as fatal or not fatal, 3) how many attacks
#have been registered for each species.

# Summarise the number of attacks for each year
attacks_per_year = data['Year'].value_counts().sort_index()

# Determine which year had the most attacks
most_entries_year = attacks_per_year.idxmax()
most_entries_count = attacks_per_year.max()

# Summarise how many attacks are fatal and how many are not
fatal_counts = data['Fatal (Y/N)'].value_counts()

# Summarise how many attacks have been recorded for each species
attacks_per_species = data['Species'].value_counts()

# Determine which species had the most attacks
most_entries_species = (attacks_per_species.idxmax())
most_entries_count1 = attacks_per_species.max()

# Display the results
print(f"The year with the most attacks is {most_entries_year} with {most_entries_count} recorded attacks.")
print("\nFatal Counts:")
print(fatal_counts)
print("\nEntries per Species:")
print(f"The species with the most attacks is {most_entries_species} with {most_entries_count1} recorded attacks.")

#Let's visualise some of the trends with barcharts.

# Plot the first bar chart with total attacks per year
plt.bar(attacks_per_year.index, attacks_per_year.values, capsize=5)
plt.xlabel('Year')
plt.ylabel('Total Number of Attacks')
plt.show()

# Plot the second bar chart with total attacks per species
plt.bar(attacks_per_species.index, attacks_per_species.values, capsize=5)
plt.xlabel('Species')
plt.ylabel('Total Number of Attacks')
#Rotate the x-axis labels to be horizontal so we can read the species names
plt.xticks(rotation=90)
plt.show()

# Plot the third bar chart with fatal vs non-fatal attacks
plt.bar(fatal_counts.index, fatal_counts.values, capsize=5)
plt.xlabel('Fatal attack')
plt.ylabel('Total Number of Attacks')
plt.show()

#let's check if, for white sharks,
# there are any changes in the number of attacks over the years

# Filter for White sharks only
white_shark_data = data[data['Species'] == 'White']

# Group by 'Year' and count the number of attacks
white_attacks_per_year = white_shark_data.groupby('Year').size()

# Plot the fourth bar chart with White shark attacks
plt.bar(white_attacks_per_year.index, white_attacks_per_year.values, capsize=5)
plt.xlabel('Year')
plt.ylabel('Total Number of White shark Attacks')
plt.show()

#let's check the same for Tiger sharks

# Filter for tiger sharks only
tiger_shark_data = data[data['Species'] == 'Tiger']

# Group by 'Year' and count the number of attacks
tiger_attacks_per_year = tiger_shark_data.groupby('Year').size()

# Plot the fifth bar chart with Tiger shark attacks
plt.bar(tiger_attacks_per_year.index, tiger_attacks_per_year.values, capsize=5)
plt.xlabel('Year')
plt.ylabel('Total Number of Tiger Shark Attacks')
plt.show()


#let's check the same for Bull sharks

# Filter for Bull sharks only
bull_shark_data = data[data['Species'] == 'Bull']

# Group by 'Year' and count the number of attacks
bull_attacks_per_year = bull_shark_data.groupby('Year').size()

# Plot the sixth bar chart with Bull shark attacks
plt.bar(bull_attacks_per_year.index, bull_attacks_per_year.values, capsize=5)
plt.xlabel('Year')
plt.ylabel('Total Number of Bull Shark Attacks')
plt.show()


#We can check if there is a difference in fatal vs non fatal attacks
#for white sharks over the years

# Group by year and 'Fatal (Y/N)' and count the number of attacks
white_fatal_counts_per_year = white_shark_data.groupby(['Year', 'Fatal (Y/N)']).size().unstack(fill_value=0)

# count the number of 'Fatal Y' and 'Fatal N' attacks for each year
white_years = white_fatal_counts_per_year.index
white_fatal_y = white_fatal_counts_per_year['Y']
white_fatal_n = white_fatal_counts_per_year['N']

#make the plot for white sharks
plt.bar(white_years, white_fatal_y, label='Fatal Y', color='red')
plt.bar(white_years, white_fatal_n, bottom=white_fatal_y, label='Fatal N', color='green')
plt.xlabel('Year')
plt.ylabel('Total Number of White Shark Attacks')
plt.legend(title='Fatal')
plt.tight_layout()
plt.show()

#we can check if there is a difference in fatal vs non fatal attacks
#for tiger sharks over the years

# Group by year and 'Fatal (Y/N)' and count the number of attacks
tiger_fatal_counts_per_year = tiger_shark_data.groupby(['Year', 'Fatal (Y/N)']).size().unstack(fill_value=0)

# count the number of 'Fatal Y' and 'Fatal N' attacks for each year
tiger_years = tiger_fatal_counts_per_year.index
tiger_fatal_y = tiger_fatal_counts_per_year['Y']
tiger_fatal_n = tiger_fatal_counts_per_year['N']

#plot for tiger sharks
plt.bar(tiger_years, tiger_fatal_y, label='Fatal Y', color='red')
plt.bar(tiger_years, tiger_fatal_n, bottom=tiger_fatal_y, label='Fatal N', color='green')
plt.xlabel('Year')
plt.ylabel('Total Number of Tiger Shark Attacks')
plt.legend(title='Fatal')
plt.tight_layout()
plt.show()

#we can check if there is a difference in fatal vs non fatal attacks
#for bull sharks over the years

# Group by year and 'Fatal (Y/N)' and count the number of attacks
bull_fatal_counts_per_year = bull_shark_data.groupby(['Year', 'Fatal (Y/N)']).size().unstack(fill_value=0)

# count the number of 'Fatal Y' and 'Fatal N' attacks for each year
bull_years = bull_fatal_counts_per_year.index
bull_fatal_y = bull_fatal_counts_per_year['Y']
bull_fatal_n = bull_fatal_counts_per_year['N']

#plot for bull sharks
plt.bar(bull_years, bull_fatal_y, label='Fatal Y', color='red')
plt.bar(bull_years, bull_fatal_n, bottom=bull_fatal_y, label='Fatal N', color='green')
plt.xlabel('Year')
plt.ylabel('Total Number of Bull Shark Attacks')
plt.legend(title='Fatal')
plt.tight_layout()
plt.show()

#Let's create some maps to visualise some of the trends from above
#We'll make the maps for the same three species

# First, we group by latitude and longitude to count the number of attacks for each of the
# three species and for each country
white_grouped = white_shark_data.groupby(['latitude', 'longitude']).size().reset_index(name='counts')
tiger_grouped = tiger_shark_data.groupby(['latitude', 'longitude']).size().reset_index(name='counts')
bull_grouped = bull_shark_data.groupby(['latitude', 'longitude']).size().reset_index(name='counts')

# Then , we create the GeoDataFrames for each species
white_gdf = gpd.GeoDataFrame(
    white_grouped, geometry=gpd.points_from_xy(white_grouped.longitude, white_grouped.latitude))
tiger_gdf = gpd.GeoDataFrame(
    tiger_grouped, geometry=gpd.points_from_xy(tiger_grouped.longitude, tiger_grouped.latitude))
bull_gdf = gpd.GeoDataFrame(
    bull_grouped, geometry=gpd.points_from_xy(bull_grouped.longitude, bull_grouped.latitude))


# We need to load a world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot the world map for White sharks, with multiplied counts by 10 for better visibility
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey')
white_gdf.plot(ax=ax, color='red', markersize=white_gdf['counts']*10)
plt.title('Locations of White Shark attacks')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Plot the world map for Tiger sharks, with multiplied counts by 10 for better visibility
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey')
tiger_gdf.plot(ax=ax, color='blue', markersize=tiger_gdf['counts']*10)
plt.title('Locations of Tiger Shark attacks')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Plot the world map for Bull sharks, with multiplied counts by 10 for better visibility
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey')
bull_gdf.plot(ax=ax, color='green', markersize=bull_gdf['counts']*10)
plt.title('Locations of Bull Shark attacks')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()


#We will create a heatmap to show the distribution of all shark attacks over the years,
#with markers that provide detailed information on how many attacks for each species, and how many
#of these attacks are fatal or non-fatal. We also specify the Country and the Area within the country

#First, we group the data by location and count the number of shark attacks for each location
location_counts = data.groupby(['Country', 'Area', 'latitude', 'longitude']).size().reset_index(name='counts')

# We then group the data by species and count the number of attacks for each species
species_counts = data.groupby(['Country', 'Area', 'Species']).size().reset_index(name='species_counts')

# We also need to group the data by whether the attacks were fatal
# and count the number for each category
fatal_counts = data.groupby(['Country', 'Area', 'Fatal (Y/N)']).size().reset_index(name='fatal_counts')

# This creates a base map
m = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=2)

# This creates the heatmap layer
heat_data = [[row['latitude'], row['longitude'], row['counts']] for index, row in location_counts.iterrows()]
HeatMap(heat_data).add_to(m)

# We then add markers with popups for each location (Based on the County and the Area)
# with detailed information on how many attacks for each species,
# and how many in total were fatal or not
for index, row in location_counts.iterrows():
    # We specify attacks for each species for the location
    species_info = species_counts[
        (species_counts['Country'] == row['Country']) & (species_counts['Area'] == row['Area'])]
    species_text = '<br>'.join(
        [f"{row['Species']}: {row['species_counts']}" for index, row in species_info.iterrows()])

    # We specify fatal vs non-fatal attacks for the location
    fatal_info = fatal_counts[
        (fatal_counts['Country'] == row['Country']) & (fatal_counts['Area'] == row['Area'])]
    fatal_text = '<br>'.join(
        [f"{row['Fatal (Y/N)']}: {row['fatal_counts']}" for index, row in fatal_info.iterrows()])

    # We combine info from number of attacks per species
    # and total fatal vs non-fatal attacks
    popup_text = f"Country: {row['Country']}<br>Area: {row['Area']}<br>Count: {row['counts']}<br>{species_text}<br>{fatal_text}"
    folium.Marker(
location = [row['latitude'], row['longitude']],
popup = popup_text
).add_to(m)

# Finally, we save the map as an HTML file. This can be opened in Pycharm by right-clicking
#on the file, open -> browser of choice
m.save('heatmap_with_detailed_markers.html')

