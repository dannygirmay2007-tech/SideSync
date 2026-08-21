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

@app.route("/generate-teams",methods=["POST"])
def generate_teams():
    '''
    Function is to generate teams. 
    args= none
    return: N/A For now
    '''
    player_ids = request.form.getlist("player_ids")
    if len(player_ids)<=1:
        return "Not enough players"
    if len(player_ids)%2!=0:
        return "Uneven players.(Perhaps play with 1 neutral?)"
    # Form values come in as strings, so convert each player ID to an integer
    player_ids = [int(value) for value in player_ids]
    # Query the database for every Player whose ID was selected
    # .where(...in_(player_ids)) filters the Player table to only those IDs
    selected_players = db.session.execute(
    # Generate every possible Team A containing half of the selected players
    db.select(Player).where(Player.id.in_(player_ids))).scalars().all()
    possible_team_as = combinations(selected_players,len(selected_players)//2)
    # Store the fairest matchup found so far
    best_diff = None
    best_a_team = None
    best_b_team= None
    # Check every possible Team A
    for team_a in possible_team_as:
        # Reset rating totals for each new matchup
        A_iq = 0
        A_tech = 0
        A_athleticism = 0
        B_iq = 0
        B_tech = 0
        B_athleticism = 0
         # Every matchup appears twice with the teams flipped.
        # Keep only combinations where the first selected player is on Team A.

        if selected_players[0] not in team_a:
            continue
        # Team B is every selected player who is NOT already on Team A
        team_b = [player for player in selected_players if player not in team_a]

        # Add together Team A's ratings
        for player in team_a:
            A_iq+= player.football_iq
            A_tech+= player.technical
            A_athleticism+= player.athleticism
            #print("A",player.name)
        # Calculate Team A's average ratings
        A_iq_avg = A_iq/len(team_a)
        A_tech_avg = A_tech/len(team_a)
        A_athleticism_avg = (A_athleticism/len(team_a))
        #print(A_iq_avg,A_tech_avg,A_athleticism_avg)
        #print("-")
        # Add together Team B's ratings
        for player in team_b:
            B_iq+= player.football_iq
            B_tech+= player.technical
            B_athleticism+= player.athleticism
            #print("B",player.name)
        # Calculate Team B's average ratings
        B_iq_avg = B_iq/len(team_b)
        B_tech_avg = B_tech/len(team_b)
        B_athleticism_avg = B_athleticism/len(team_b)
        #print(B_iq_avg,B_tech_avg,B_athleticism_avg)
        # Calculate the difference between the teams in each category.
        # abs() makes the difference positive no matter which team is stronger.
        # Apply our weights: IQ 45%, Technical 35%, Athleticism 20%.
        
        iq_diff = abs((A_iq_avg*0.45) - (B_iq_avg*0.45))
        tech_diff = abs((A_tech_avg*0.35) - (B_tech_avg*0.35))
        athleticism_diff = abs((A_athleticism_avg*0.20) - (B_athleticism_avg*0.20))
        # One overall balance penalty.
        # Lower total_diff means the teams are more evenly matched.
        total_diff = iq_diff+tech_diff+athleticism_diff
        if best_diff is None or total_diff < best_diff:
            best_diff = total_diff
            best_a_team= [player for player in team_a]
            best_b_team = [player for player in team_b]
            
        #print("***\n",iq_diff,tech_diff,athleticism_diff)
        #print("------")
    # After checking every matchup, these are the fairest teams found    
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