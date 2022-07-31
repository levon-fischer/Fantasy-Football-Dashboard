import requests
import pandas as pd

league_ids = {'2020': '599772937209298944', '2021': '725924134428712960', '2022': '784428347810816000'}


def main():
    users = pd.DataFrame(columns=['display_name', 'user_id', 'team_name'])
    rosters = pd.DataFrame(columns=['year', 'owner_id', 'roster_id', 'wins', 'losses'])
    trades = pd.DataFrame(columns=['year', 'roster_ids', 'creator', 'consenter', 'week', 'adds',
                                   'drops', 'draft_picks', 'waiver_budget'])

    for year in league_ids:
        new_users = get_users(year)
        new_rosters = get_rosters(year)
        new_trades = get_trades(year)
        # get_traded_picks(year)

        users = pd.concat([users, new_users], ignore_index=True)
        rosters = pd.concat([rosters, new_rosters], ignore_index=True)
        trades = pd.concat([trades, new_trades], ignore_index=True)

    print(rosters)
    print(users)
    print(trades.head())


# -----Functions---------------------------------------------------------------------------------------------------------
def get_users(year):
    users_response = requests.get('https://api.sleeper.app/v1/league/' + league_ids[year] + '/users').json()

    user_list = []
    for user in users_response:
        if 'team_name' in user['metadata']:
            user_list.append([user['display_name'], user['user_id'], user['metadata']['team_name']])
        else:
            user_list.append([user['display_name'], user['user_id'], None])

    users_df = pd.DataFrame(data=user_list, columns=['display_name', 'user_id', 'team_name'])
    return users_df


def get_rosters(year):
    rosters_response = requests.get('https://api.sleeper.app/v1/league/' + league_ids[year] + '/rosters').json()
    roster_list = []
    for roster in rosters_response:
        roster_list.append([year, roster['owner_id'], roster['roster_id'],
                            roster['settings']['wins'], roster['settings']['losses']])
    rosters_df = pd.DataFrame(data=roster_list, columns=['year', 'owner_id', 'roster_id', 'wins', 'losses'])
    return rosters_df


def get_trades(year):
    week = 1
    trade_list = []
    for i in range(17):
        trades_response = requests.get('https://api.sleeper.app/v1/league/' + league_ids[year] +
                                       '/transactions/' + str(week)).json()
        for trade in trades_response:
            if trade['type'] == 'trade':
                trade_list.append([year, trade['roster_ids'], trade['creator'], trade['consenter_ids'], trade['leg'],
                                   trade['adds'], trade['drops'], trade['draft_picks'], trade['waiver_budget']])
        week += 1

    trades_df = pd.DataFrame(data=trade_list, columns=['year', 'roster_ids', 'creator', 'consenter', 'week', 'adds',
                                                       'drops', 'draft_picks', 'waiver_budget'])
    return trades_df


def get_matchups(year):
    week = 1
    matchup_list = []
    for i in range(17):
        matchup_response = requests.get(
            'https://api.sleeper.app/v1/league/' + league_ids[year] + '/matchups/' + str(week)).json()

        week += 1


# def get_traded_picks(year_id):
# traded_picks = requests.get('https://api.sleeper.app/v1/league/' + year_id + '/traded_picks').json()
# picks_list = []
# for trade in traded_picks:

#-----Execute the program-----------------------------------------------------------------------------------------------

main()
# user_id
# display_name
# metadata team_name
