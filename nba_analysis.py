import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv('NBA_2024_per_game.csv')

print(df.head())
print(df.describe())

def clean_data(df):
    df = df.drop(columns=['G', 'GS', 'MP', 'FG', 'FGA', '2P','2PA', 'FT', 'FTA'], errors='ignore')
    df.rename(columns={'Rk': 'Rank', 'Pos': 'Position', 'Tm': 'Team', 'TRB': 'Rebounds'}, inplace=True)
    df['PTS'] = pd.to_numeric(df['PTS'], errors='coerce')
    df['AST'] = pd.to_numeric(df['AST'], errors='coerce')
    df['Rebounds'] = pd.to_numeric(df['Rebounds'], errors='coerce')
    return df.dropna()

cleaned_data = clean_data(df)
print(cleaned_data.head())

def summarize_data(df):
    print(df.describe())

summarize_data(cleaned_data)

def visualize_three_point_performance(df, player_name):
    # Filter the data for the specific player
    player_data = df[df['Player'] == player_name]

    # Check if the necessary columns exist
    if '3P' in player_data.columns and '3PA' in player_data.columns:
        # Create a scatter plot with a regression line
        plt.figure(figsize=(12, 6))
        sns.set_palette("bright")

        # Scatter plot for shots made vs. attempts
        sns.scatterplot(x='3PA', y='3P', data=player_data, s=100, alpha=0.6, label='Shots Made')

        # Line plot for progression
        plt.plot(player_data['3PA'], player_data['3P'], color='blue', linestyle='-', linewidth=2,
                 label='Progression Line')

        # Adding titles and labels
        plt.title('Three-Point Attempts vs. Made', fontsize=18, fontweight='bold')
        plt.xlabel('Three-Point Attempts (3PA)', fontsize=14)
        plt.ylabel('Three-Point Shots Made (3PM)', fontsize=14)
        plt.grid(True)
        plt.legend()
        plt.show()

# Call the function with the player you want to analyze
visualize_three_point_performance(cleaned_data, "Anthony Edwards")

