import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import glob
import numpy as np


# Use glob to find all CSV files in a directory
path = './statsheets/'
csv_files = glob.glob(path + '*.csv')  # Get all CSV files in the directory

# Initialize an empty list to store each CSV DataFrame
data_frames = []

# Loop through the list of CSV files and read each one
for file in csv_files:
    df = pd.read_csv(file)  # Read each CSV
    data_frames.append(df)  # Append to list

# Concatenate all DataFrames into a single DataFrame
all_player_data = pd.concat(data_frames, ignore_index=True)

# Remove non-numeric entries from 'MP' column and replace with NaN for numeric conversion
all_player_data = all_player_data[~all_player_data['MP'].isin(['Inactive', 'Did Not Play', 'Did Not Dress'])]

# Convert columns to numeric, invalid parsing will be set as NaN
all_player_data['PTS'] = pd.to_numeric(all_player_data['PTS'], errors='coerce')
all_player_data['FG%'] = pd.to_numeric(all_player_data['FG%'], errors='coerce')
all_player_data['AST'] = pd.to_numeric(all_player_data['AST'], errors='coerce')
all_player_data['TRB'] = pd.to_numeric(all_player_data['TRB'], errors='coerce')

# Drop any rows with NaN values
all_player_data.dropna(subset=['PTS', 'FG%', 'AST', 'TRB'], inplace=True)

# Separate features and target variable
X = all_player_data[['PTS', 'FG%', 'AST', 'TRB']]
y = all_player_data['PTS']




# Load your regular season data
player_data_regular = pd.read_csv('statsheets/naz_raid_23_24.csv')

# Load playoff data
player_data_playoff = pd.read_csv('statsheets/nazreid2324playoffs.csv')

# Add a column to differentiate regular season and playoff games
player_data_regular['Game Type'] = 'Regular Season'
player_data_playoff['Game Type'] = 'Playoffs'

# Combine both datasets
player_data = pd.concat([player_data_regular, player_data_playoff], ignore_index=True)

# Streamlit app title
st.title('Naz Reid 23-24 Season Stats')

# Add a link to the source of your stats
st.markdown('[Stats sourced from Basketball Reference](basketball-reference.com)')

# Mapping display names to actual column names
stat_map = {
    'Points per Game': 'PTS',
    'Rebounds per Game': 'TRB',
    'Assists per Game': 'AST',
    '3-Point Attempts': '3PA',
    '3-Points Made': '3P'
}

# Display the stat options in the dropdown
selected_display_stat = st.selectbox('Select a stat to display:', list(stat_map.keys()))

# Get the corresponding column name from the mapping
selected_stat_column = stat_map[selected_display_stat]

# Calculate average of the selected stat
average_stat = player_data[selected_stat_column].mean()

# Drop or fill missing values as needed
player_data.fillna(0, inplace=True)

# Create a color palette for different game types
palette = {
    'Regular Season': '#0C2340',
    'Playoffs': '#78BE20',  # You can further differentiate playoff rounds
    # 'In-Season Tournament': 'green',  # Uncomment if you have this data
}

# Set up the plot
fig, ax = plt.subplots(figsize=(16, 8))
fig.patch.set_facecolor('#f0f0f0')  # figure background
ax.set_facecolor('#236192')  # axes background

# Plot the data with different colors based on the game type
for game_type in player_data['Game Type'].unique():
    # Filter data for the current game type
    game_data = player_data[player_data['Game Type'] == game_type]

    # Plot the line for the current game type
    sns.lineplot(
        x='G',
        y=selected_stat_column,
        data=game_data,
        marker='o',
        ax=ax,
        label=game_type,
        color=palette.get(game_type, 'grey'),  # Default color if not found
        markeredgecolor=palette.get(game_type, 'grey'),
        zorder=1
    )

# Highlight the 6th man game with a star marker
star_game_number = 85
star_stat_value = player_data[selected_stat_column].iloc[star_game_number - 1]  # Adjust for 0-indexing
ax.scatter(star_game_number, star_stat_value, color='gold', s=100, marker='*', label='Sixth Man Award Game', zorder=2)

# Highlight the towel giveaway game with a diamond marker
diamond_game_number = 70
diamond_stat_value = player_data[selected_stat_column].iloc[diamond_game_number - 1]  # Adjust for 0-indexing
ax.scatter(diamond_game_number, diamond_stat_value, color='#c0dfd3', s=100, marker='d', label='Towel Giveaway Game', zorder=2, edgecolor='#0C2340')

# Average stat line
ax.axhline(y=average_stat, color='red', linestyle='--', label=f'Average {selected_display_stat}')

# Adding titles and labels
ax.set_title(f'{selected_display_stat} Over the 23-24 Season', fontsize=18, fontweight='bold')
ax.set_xlabel('Game', fontsize=14)
ax.set_ylabel(selected_stat_column, fontsize=14)

# Show labels every 5 games on the x-axis
game_numbers = player_data['G']
ax.set_xticks(game_numbers[::5])
ax.set_xticklabels(game_numbers[::5], rotation=45)

ax.grid(True, alpha=0.3)
ax.legend()

# Position the average value on the side of the plot
ax.text(len(player_data['G']) + 8, average_stat - 1, f'{average_stat:.2f}',
        color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='right')

# Show plot in Streamlit
st.pyplot(fig)

# Split the data into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
print(f"RMSE: {rmse}")

# Predict PPG for a new season based on previous season stats
new_season_data = pd.DataFrame({
    'PTS': [19.99],  # Example data for a player
    'FG%': [0.45],
    'AST': [5],
    'TRB': [8]
})

# display the result
predicted_ppg_array = model.predict(new_season_data)
predicted_ppg = round(float(predicted_ppg_array[0]), 2)  # Round it to two decimal places

current_ppg = 13.06
# Create your plot
plt.figure(figsize=(10, 5))
plt.bar(['Current PPG', 'Predicted PPG'], [current_ppg, predicted_ppg])
plt.ylabel('Points Per Game')
plt.title('Current vs. Predicted PPG')
st.pyplot(plt)  # Display the plot in Streamlit

# Display the rounded prediction beneath the plot
st.write(f"Predicted PPG for the next season: {predicted_ppg}")




