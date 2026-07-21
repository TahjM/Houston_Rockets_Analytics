import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import teamgamelog
import matplotlib.pyplot as plt
from nba_api.stats.endpoints import boxscoresummaryv3
import time
# get Rockets team id

nba_teams = teams.get_teams()
rockets = [t for t in nba_teams if t[ 'abbreviation'] == 'HOU'][0]
print(rockets)

gamelog = teamgamelog.TeamGameLog(team_id=1610612745, season='2025-26')
df = gamelog.get_data_frames()[0]
print(df.head)
print(df.shape)
print(df.columns.tolist())

# get home record
df_Home = df[df['MATCHUP'].str.contains('vs.')]
print(df_Home.shape)
print(df_Home[['MATCHUP', 'WL']].head())
print(df_Home[['WL']].value_counts())

# get away record
df_AWAY = df[df['MATCHUP'].str.contains('@')]
print(df_AWAY.shape)
print(df_AWAY[['MATCHUP', 'WL']].head())
print(df_AWAY[['WL']].value_counts())

# Chart home and away win pct

home_win_pct = 30/41
away_win_pct = 22/41

plt.bar(['Home', 'Away'], [home_win_pct, away_win_pct])
plt.ylabel('Win %')
plt.title('Rockets 2025-26: Home vs Away Win %')
plt.ylim(0,1)
plt.show()

# pull first games line score
game_id = '0022501194' # first game id
summary = boxscoresummaryv3.BoxScoreSummaryV3(game_id=game_id)
dfs = summary.get_data_frames()

for i, d in enumerate(dfs):
    print(i, d.columns.tolist())

# inspect the line score data frame
line_score = dfs[4]
print(line_score)

""""# calculate point differential for each quarter from game 1
hou_row = line_score[line_score['teamId'] == 1610612745].iloc[0]
mem_row = line_score[line_score['teamId'] == 1610612763].iloc[0]

for q in range(1,5):
    col = f'period{q}Score'
    diff = hou_row[col] - mem_row[col]
    print(f"Q{q} diiferential: {diff}")"""


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

get_quarter_diff('0022501194')

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

# get
merged_df['Final Margin'] = merged_df['Q1_diff'] + merged_df['Q2_diff'] + merged_df['Q3_diff'] + merged_df['Q4_diff']
merged_df['Close games'] = merged_df['Final Margin'].abs() <= 5

close_games_df = merged_df[merged_df['Close games']]
print("close games")
print(close_games_df.shape)
print(close_games_df[['MATCHUP', 'WL']].head())
print(close_games_df[['WL']].value_counts())





# get avg differential for each quarter
diff_averages = merged_df[['Q1_diff', 'Q2_diff', 'Q3_diff', 'Q4_diff']].mean()
print(diff_averages)

plt.bar(['Q1', 'Q2', 'Q3', 'Q4'], [1.48, 1.91, 2.45, -0.43],)
plt.ylabel('Point Differential')
plt.title('Quarter differentials')
plt.ylim(-1,3)
plt.show()

final_df = merged_df[['gameId', 'MATCHUP', 'GAME_DATE', 'WL', 'Q1_diff', 'Q2_diff', 'Q3_diff', 'Q4_diff','Final Margin', 'Close games']]
final_df.to_csv('data/Rockets_2025_26.csv',  encoding='utf-8', index=False)
