from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# API details
API_KEY = '0d5d4d5a6c4c4347896157968861deb4'
BASE_URL = 'https://api.football-data.org/v4/'
HEADERS = {'X-Auth-Token': API_KEY}

def get_teams():
    """Fetch all teams in the English Premier League."""
    response = requests.get(BASE_URL + 'competitions/PL/teams', headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('teams', [])
    else:
        return []

def get_players(team_id):
    """Fetch players for a specific team using its team ID."""
    response = requests.get(f'{BASE_URL}teams/{team_id}', headers=HEADERS)
    if response.status_code == 200:
        return response.json().get('squad', [])
    else:
        return []

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/team', methods=['POST'])
def team():
    """Handle team search and display team details."""
    team_name = request.form['team_name']
    teams = get_teams()
    for team in teams:
        if team_name.lower() in team['name'].lower():
            return render_template('team.html', team=team)
    return f"No team found with the name '{team_name}'."

@app.route('/player', methods=['POST'])
def player():
    """Handle player search and display player details."""
    team_name = request.form['team_name']
    player_name = request.form['player_name']

    # Find team
    teams = get_teams()
    for team in teams:
        if team_name.lower() in team['name'].lower():
            team_id = team['id']
            # Find player in the team
            players = get_players(team_id)
            for player in players:
                if player_name.lower() in player['name'].lower():
                    return render_template('player.html', player=player, team_name=team['name'])
            return f"No player found with the name '{player_name}' in {team['name']}."
    return f"No team found with the name '{team_name}'."

if __name__ == '__main__':
    app.run(debug=True)
