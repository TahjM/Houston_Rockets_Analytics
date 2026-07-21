import pandas as pd
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import boxscoresummaryv3
import time

gamelog = teamgamelog.TeamGameLog(team_id=1610612745, season='2025-26')
df = gamelog.get_data_frames()[0]
print(df.head)
print(df.shape)
print(df.columns.tolist())


# get quarter differential for each game
def get_quarter_diff(game_id):
    summary = boxscoresummaryv3.BoxScoreSummaryV3(game_id=game_id)
    line_score = summary.get_data_frames()[4]

    hou_row = line_score[line_score['teamId'] == 1610612745].iloc[0]
    opp_row = line_score[line_score['teamId'] != 1610612745].iloc[0]

    diffs = {'gameId': game_id}
    for q in range(1,5):
        col = f'period{q}Score'
        diffs[f'Q{q}_diff'] = hou_row[col] - opp_row[col]

    return diffs


# loop through all 82 regular season games
all_games = []

for game_id in df['Game_ID']:
    try:
        diffs = get_quarter_diff(game_id)
        all_games.append(diffs)
    except Exception as e:
        print(f"Failed on {game_id}: {e}")
    time.sleep(0.6)

quarter_df = pd.DataFrame(all_games)
print(quarter_df.shape)
print(quarter_df.head())

# merge data from each quarter with the game logs
merged_df = pd.merge(quarter_df, df, left_on='gameId', right_on='Game_ID')
print(merged_df.shape)
print(merged_df[['GAME_DATE', 'MATCHUP', 'WL', 'Q1_diff', 'Q2_diff', 'Q3_diff', 'Q4_diff']].head())

final_df = merged_df[['gameId', 'MATCHUP', 'GAME_DATE', 'WL', 'Q1_diff', 'Q2_diff', 'Q3_diff', 'Q4_diff']]
final_df.to_csv('data/Rockets_2025_26.csv',  encoding='utf-8', index=False)
