import pandas as pd

import geopandas as gpd
import matplotlib.pyplot as plt


# Replace the file path to 'attacks.csv' with the path to your CSV file.
# I loaded the repository manually, by saving the CSV file within my assessment folder
file_path = 'attacks.csv'

# Load the CSV file
data = pd.read_csv(file_path)


# Display the first few rows of the dataframe
print(data.head())

# Despite having done extensive cleaning manually,
# there are still some problems: strip whitespace from the column names
data.columns = data.columns.str.strip()
# Standardize the species names to ensure consistency
data['Species'] = data['Species'].str.strip().str.lower().str.title()
# Clean the 'Fatal (Y/N)' column
data['Fatal (Y/N)'] = data['Fatal (Y/N)'].str.strip().str.upper()

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
print("Attacks per Year:")
print(attacks_per_year)
print(f"The year with the most attacks is {most_entries_year} with {most_entries_count} recorded attacks.")
print("\nFatal Counts:")
print(fatal_counts)
print("\nEntries per Species:")
print(attacks_per_species)
print(f"The species with the most attacks is {most_entries_species} with {most_entries_count1} recorded attacks.")

#Let's visualise some of the trends with barcharts. All barcharts show mean +- SE

# Calculate the mean and standard error of the attacks per year
mean_attacks = attacks_per_year.mean()
std_error = attacks_per_year.sem()

# Plot the first bar chart with attacks per year
plt.figure(1)
plt.bar(attacks_per_year.index, attacks_per_year.values, yerr=std_error, capsize=5)
plt.title('Mean and Standard Error of Attacks Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Attacks')
plt.show()


# Calculate the mean and standard error of the attacks per species
mean_attacks_species = attacks_per_species.mean()
std_error_species = attacks_per_species.sem()

# Plot the second bar chart with attacks per species
plt.figure(2)
plt.bar(attacks_per_species.index, attacks_per_species.values, yerr=std_error_species, capsize=5)
plt.title('Mean and Standard Error of Attacks Per Species')
plt.xlabel('Species')
plt.ylabel('Number of Attacks')
# Rotate the x-axis labels to be horizontal
plt.xticks(rotation=90)
plt.show()


# Filter out any rows where 'Fatal (Y/N)' is not 'Y' or 'N'
data = data[data['Fatal (Y/N)'].isin(['Y', 'N'])]

# Calculate the mean and standard error for 'Fatal (Y/N)'
mean_attacks_fatal = fatal_counts.mean()
std_error_fatal = fatal_counts.sem()

# Plot the third bar chart with fatal vs non-fatal attacks
plt.figure(3)
plt.bar(fatal_counts.index, fatal_counts.values, yerr=std_error_fatal, capsize=5)
plt.title('Mean and Standard Error of fatal vs non fatal attacks')
plt.xlabel('Fatal attack')
plt.ylabel('Number of Attacks')
plt.show()

#let's check if, for white sharks,
# there are any changes in the number of attacks over the years

# Filter for White sharks only
white_shark_data = data[data['Species'] == 'White']

# Group by 'Year' and count the number of attacks
white_attacks_per_year = white_shark_data.groupby('Year').size()

# Calculate the mean and standard error
mean_attacks_white = white_attacks_per_year.mean()
std_error_white = white_attacks_per_year.sem()

# Plot the third bar chart with White shark attacks
plt.figure(4)
plt.bar(white_attacks_per_year.index, white_attacks_per_year.values, yerr=std_error_white, capsize=5)
plt.title('Mean and Standard Error of White sharks attacks over the years')
plt.xlabel('Year')
plt.ylabel('Number of White shark Attacks')
plt.show()

#let's check the same for Tiger sharks

# Filter for tiger sharks only
tiger_shark_data = data[data['Species'] == 'Tiger']

# Group by 'Year' and count the number of attacks
tiger_attacks_per_year = tiger_shark_data.groupby('Year').size()

# Calculate the mean and standard error
mean_attacks_tiger = tiger_attacks_per_year.mean()
std_error_tiger = tiger_attacks_per_year.sem()

# Plot the fifth bar chart with Tiger shark attacks
plt.figure(5)
plt.bar(tiger_attacks_per_year.index, tiger_attacks_per_year.values, yerr=std_error_tiger, capsize=5)
plt.title('Mean and Standard Error of Tiger sharks attacks over the years')
plt.xlabel('Year')
plt.ylabel('Number of Bull shark Attacks')
plt.show()

#let's check the same for Bull sharks

# Filter for Bull sharks only
bull_shark_data = data[data['Species'] == 'Bull']

# Group by 'Year' and count the number of attacks
bull_attacks_per_year = bull_shark_data.groupby('Year').size()

# Calculate the mean and standard error for 'Fatal (Y/N)'
mean_attacks_bull = bull_attacks_per_year.mean()
std_error_bull = bull_attacks_per_year.sem()

# Plot the third bar chart with fatal vs non-fatal attacks
plt.figure(6)
plt.bar(bull_attacks_per_year.index, bull_attacks_per_year.values, yerr=std_error_bull, capsize=5)
plt.title('Mean and Standard Error of Bull sharks attacks over the years')
plt.xlabel('Year')
plt.ylabel('Number of Bull shark Attacks')
plt.show()

#Let's create some plot to visualise some of the trends from above
#We'll plot for the three most likely species

# Group by latitude and longitude to count the number of attacks for each species and for each country
white_grouped = white_shark_data.groupby(['latitude', 'longitude']).size().reset_index(name='counts')
tiger_grouped = tiger_shark_data.groupby(['latitude', 'longitude']).size().reset_index(name='counts')
bull_grouped = bull_shark_data.groupby(['latitude', 'longitude']).size().reset_index(name='counts')

# Create the GeoDataFrames for each species
white_gdf = gpd.GeoDataFrame(
    white_grouped, geometry=gpd.points_from_xy(white_grouped.longitude, white_grouped.latitude))
tiger_gdf = gpd.GeoDataFrame(
    tiger_grouped, geometry=gpd.points_from_xy(tiger_grouped.longitude, tiger_grouped.latitude))
bull_gdf = gpd.GeoDataFrame(
    bull_grouped, geometry=gpd.points_from_xy(bull_grouped.longitude, bull_grouped.latitude))


# Load a world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot the world map for White sharks, but multiplied counts by 10 for better visibility
fig, ax = plt.subplots(figsize=(15, 10))
world.plot(ax=ax, color='lightgrey')
white_gdf.plot(ax=ax, color='red', markersize=white_gdf['counts']*10)
plt.title('Locations of White Shark attacks')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# Plot the world map for Tiger sharks, but multiplied counts by 10 for better visibility
#fig, ax = plt.subplots(figsize=(15, 10))
#world.plot(ax=ax, color='lightgrey')
#tiger_gdf.plot(ax=ax, color='blue', markersize=tiger_gdf['counts']*10)
#plt.title('Locations of Tiger Shark attacks')
#plt.xlabel('Longitude')
#plt.ylabel('Latitude')
#plt.show()

# Plot the world map for Bull sharks, but multiplied counts by 10 for better visibility
#fig, ax = plt.subplots(figsize=(15, 10))
#world.plot(ax=ax, color='lightgrey')
#bull_gdf.plot(ax=ax, color='green', markersize=bull_gdf['counts']*10)
#plt.title('Locations of Bull Shark attacks')
#plt.xlabel('Longitude')
#plt.ylabel('Latitude')
#plt.show()




