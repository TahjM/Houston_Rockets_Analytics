import matplotlib.pyplot as plt

# chart for quarter differentials
def plot_quarter_diffs(diff_averages):
    plt.figure()
    bars = plt.bar(['Q1', 'Q2', 'Q3', 'Q4'], diff_averages, color='#C4CED4')
    plt.bar_label(bars, fmt='%.2f', color='#CE1141')
    plt.ylabel('Point differential')
    plt.title('Quarter differentials')
    plt.ylim(-1, 3)
    plt.axhline(y=0, color='black', linewidth=0.8)

    plt.savefig('data/quarter_diff_chart.png')

# chart for win percentage
def plot_win_pct(win_pct):
    plt.figure()
    bars = plt.bar(['Home', 'Away'], win_pct, color='#C4CED4')
    plt.bar_label(bars, fmt='%.1f', color='#CE1141')
    plt.ylabel('Win percentage')
    plt.title('Home vs. Away Win Percentage')
    plt.ylim(0,100)
    plt.savefig('data/win_pct_chart.png')

# chart for close games win pct
def plot_close_games_win_pct(close_games_win_pct):
    plt.figure()
    bars = plt.bar(['Home', 'Away'], close_games_win_pct, color='#C4CED4')
    plt.bar_label(bars, fmt='%.1f', color='#CE1141')
    plt.ylabel('Win percentage')
    plt.title('Home vs. Away Close Games Win Percentage')
    plt.ylim(0,100)
    plt.savefig('data/close_games_win_pct_chart.png')

# chart for close games win and losses
def plot_close_games(close_games):
    plt.figure()
    bars = plt.bar(['wins', 'losses'], close_games, color='#C4CED4')
    plt.bar_label(bars, color='#CE1141')
    plt.title('Close Games Record')
    plt.ylim(0, 25)
    plt.savefig('data/close_games_chart.png')

