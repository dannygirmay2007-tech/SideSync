from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from itertools import combinations

'''
app is defining the app uses Flask object.
app.config line defines where sqlite is stored
db is defining it as a SQLAlchemy object.
'''
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sidesync.db"
db = SQLAlchemy(app)

class Player(db.Model):
    '''
    model for a player table.
    it inherits models from db aka SQLAlchemy
    
    '''
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)
    athleticism = db.Column(db.Float, nullable= False)
    technical = db.Column(db.Float, nullable= False)
    football_iq = db.Column(db.Float, nullable= False)

@app.route("/", methods=["GET","POST"])
def home():
    '''
    Post takes in info from the submission.
    Get only asks for data; it does not automatically search or fetch that data for you. 
    '''
    if request.method == "POST":
        player_name = request.form["player_name"].strip()
        '''
        new_player creates a new instance of the Player model.
        name we get from player_name because we strip right before adding it.
        athleticsm,tekk,iq all come from the reqeust.form[field]
        '''
        new_player = Player(
    name= player_name,
    athleticism=float(request.form["athleticism"]),
    technical=float(request.form["technical"]),
    football_iq=float(request.form["football_iq"])
)

        if player_name:
            '''
            add stages a pending database change 
            commit actually permanetly writes it into SQLite permanetly.
            '''
            db.session.add(new_player)
            db.session.commit()

        return redirect(url_for("home"))
    '''
    Query all saved Player records from the database:
    select Player rows → execute the query → extract Player objects → return them as a list
    '''
    players = db.session.execute(db.select(Player)).scalars().all()

    return render_template(
        "index.html",
        players=players,
        player_count=len(players)
    )
@app.route("/players/<int:player_id>/delete", methods=["POST"])
def delete_player(player_id):
    ''' Function used to delete players from db
    args: player_id
    return: home page

    '''
    player = db.session.get(Player, player_id)
    if player:
        db.session.delete(player)
        db.session.commit()
    return redirect(url_for("home"))
@app.route("/players/<int:player_id>/edit", methods=["GET", "POST"])
def edit_player(player_id):
    player = db.session.get(Player,player_id)

    if request.method == "POST":
        player_name = request.form["player_name"].strip()
        player.name = player_name
        player.athleticism=float(request.form["athleticism"])
        player.technical=float(request.form["technical"])
        player.football_iq=float(request.form["football_iq"])
        db.session.commit()
    if request.method == "GET":
        return render_template(
    "edit_player.html",
    player=player
    )
    return redirect(url_for("home"))

def balance_teams(selected_players):
    """
    Finds the most balanced possible split of the selected players.

    Args:
        selected_players: List of Player objects

    Returns:
        best_a_team: Best Team A
        best_b_team: Best Team B
        best_diff: Balance penalty for the matchup
    """

    possible_team_as = combinations(
        selected_players,
        len(selected_players) // 2
    )

    best_diff = None
    best_a_team = None
    best_b_team = None

    for team_a in possible_team_as:

        # Ignore duplicate matchups where Team A and Team B are just flipped
        if selected_players[0] not in team_a:
            continue

        team_b = [
            player
            for player in selected_players
            if player not in team_a
        ]

        team_a_iq_total = 0
        team_a_tech_total = 0
        team_a_athleticism_total = 0

        team_b_iq_total = 0
        team_b_tech_total = 0
        team_b_athleticism_total = 0

        for player in team_a:
            team_a_iq_total += player.football_iq
            team_a_tech_total += player.technical
            team_a_athleticism_total += player.athleticism

        for player in team_b:
            team_b_iq_total += player.football_iq
            team_b_tech_total += player.technical
            team_b_athleticism_total += player.athleticism

        team_a_iq_avg = team_a_iq_total / len(team_a)
        team_a_tech_avg = team_a_tech_total / len(team_a)
        team_a_athleticism_avg = team_a_athleticism_total / len(team_a)

        team_b_iq_avg = team_b_iq_total / len(team_b)
        team_b_tech_avg = team_b_tech_total / len(team_b)
        team_b_athleticism_avg = team_b_athleticism_total / len(team_b)

        iq_diff = abs(team_a_iq_avg - team_b_iq_avg) * 0.45
        tech_diff = abs(team_a_tech_avg - team_b_tech_avg) * 0.35
        athleticism_diff = (
            abs(team_a_athleticism_avg - team_b_athleticism_avg) * 0.20
        )

        total_diff = iq_diff + tech_diff + athleticism_diff

        if best_diff is None or total_diff < best_diff:
            best_diff = total_diff

            # Keep the Player objects so the template can use player.name,
            # player.technical, etc.
            best_a_team = team_a
            best_b_team = team_b

    return best_a_team, best_b_team, best_diff



@app.route("/generate-teams", methods=["POST"])
def generate_teams():
    player_ids = request.form.getlist("player_ids")

    if len(player_ids) <= 1:
        return "Not enough players"

    if len(player_ids) % 2 != 0:
        return "Uneven players. (Perhaps play with 1 neutral?)"

    player_ids = [int(value) for value in player_ids]

    selected_players = db.session.execute(
        db.select(Player).where(Player.id.in_(player_ids))
    ).scalars().all()

    best_a_team, best_b_team, best_diff = balance_teams(selected_players)

    return render_template(
        "generate_teams.html",
        best_a_team=best_a_team,
        best_b_team=best_b_team,
        best_diff=best_diff
    )
with app.app_context():
    '''
    creates any missing database tables based on my models.
    '''
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True)