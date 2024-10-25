import requests

api_key = '0d5d4d5a6c4c4347896157968861deb4'
base_url = 'https://api.football-data.org/v4/'
headers = {'X-Auth-Token': api_key}

def get_teams():
    
    """Fetch all teams in the English Premier League."""
    
    response = requests.get(base_url + 'competitions/PL/teams', headers=headers)
    
    if response.status_code == 200:
        return response.json().get('teams', [])
    else:
        print(f"Error fetching teams: {response.status_code}")
        return []

def search_team(team_name):
    
    """Search for a team by name."""
    
    teams = get_teams()
    
    for team in teams:
        if team_name.lower() in team['name'].lower():
            print(f"Team: {team['name']}")
            print(f"ID: {team['id']}")
            print(f"Venue: {team.get('venue', 'N/A')}")
            print(f"Founded: {team.get('founded', 'N/A')}")
            print(f"Website: {team.get('website', 'N/A')}")
            return team['id']  # Return the ID for further player search
    print(f"No team found with the name '{team_name}'.")
    return None

def get_players(team_id):
    
    """Fetch players for a specific team using its team ID."""
    
    response = requests.get(f'{base_url}teams/{team_id}', headers=headers)
    if response.status_code == 200:
        return response.json().get('squad', [])
    else:
        print(f"Error fetching players: {response.status_code}")
        return []

def search_player(team_id, player_name):
    
    """Search for a player by name in a specific team."""
    
    players = get_players(team_id)
    for player in players:
        if player_name.lower() in player['name'].lower():
            print(f"Player: {player['name']}")
            print(f"Position: {player.get('position', 'N/A')}")
            print(f"Nationality: {player.get('nationality', 'N/A')}")
            print(f"Date of Birth: {player.get('dateOfBirth', 'N/A')}")
            print(f"Shirt Number: {player.get('shirtNumber', 'N/A')}")
            return
    print(f"No player found with the name '{player_name}'.")

def main():
    search_type = input("Would you like to search for a 'team' or 'player'? ").strip().lower()
    
    if search_type == 'team':
        team_name = input("Enter the name of the team: ").strip()
        search_team(team_name)
    
    elif search_type == 'player':
        team_name = input("Enter the name of the team the player belongs to: ").strip()
        team_id = search_team(team_name)
        if team_id:
            player_name = input("Enter the name of the player: ").strip()
            search_player(team_id, player_name)
    
    else:
        print("Invalid search type. Please enter 'team' or 'player'.")

if __name__ == '__main__':
    main()
