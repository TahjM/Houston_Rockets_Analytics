import pandas as pd
from Visualize import plot_quarter_diffs
from Visualize import plot_win_pct
from Visualize import plot_close_games_win_pct
from Visualize import plot_close_games

data_df = pd.read_csv('data/Rockets_2025_26.csv', dtype={"gameId": str})
print(data_df.shape)
print(data_df.head())


# filter home games
df_Home = data_df[data_df['MATCHUP'].str.contains('vs.')]
print(df_Home.shape)
print(df_Home[['MATCHUP', 'WL']].head())
print(df_Home[['WL']].value_counts())

# filter away games
df_Away = data_df[data_df['MATCHUP'].str.contains('@')]
print(df_Away.shape)
print(df_Away[['MATCHUP', 'WL']].head())
print(df_Away[['WL']].value_counts())


# get quarter differential averages
diff_averages = data_df[['Q1_diff', 'Q2_diff', 'Q3_diff', 'Q4_diff']].mean()
print(diff_averages)
plot_quarter_diffs(diff_averages)


# get home & away win percentages
home_win = df_Home['WL'].value_counts()
home_win_pct = home_win['W'] / len(df_Home) * 100
away_win = df_Away['WL'].value_counts()
away_win_pct = away_win['W'] / len(df_Away) * 100
win_pct = [home_win_pct, away_win_pct]
plot_win_pct(win_pct)


# Count games that are decided by 5 or less points
data_df['Final Margin'] = (data_df['Q1_diff'] + data_df['Q2_diff'] + data_df['Q3_diff'] + data_df['Q4_diff'])
data_df['Close games'] = data_df['Final Margin'].abs() <= 5
close_games_df = data_df[data_df['Close games']]
print(close_games_df['WL'].value_counts())
closeGames = close_games_df['WL'].value_counts()
close_games_win = closeGames['W']
close_games_loss = closeGames['L']
close_games = [close_games_win, close_games_loss]
plot_close_games(close_games)


# Percentage of close game wins at home and away
close_home_df = close_games_df[close_games_df['MATCHUP'].str.contains('vs.')]
close_away_df = close_games_df[close_games_df['MATCHUP'].str.contains('@')]
close_home_win = close_home_df['WL'].value_counts()
close_away_win = close_away_df['WL'].value_counts()
close_home_pct = close_home_win['W'] / len(close_home_df) * 100
close_away_pct = close_away_win['W'] / len(close_away_df) * 100
close_games_win_pct = [close_home_pct, close_away_pct]
plot_close_games_win_pct(close_games_win_pct)

