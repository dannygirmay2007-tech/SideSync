from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    player_ids = [int(value) for value in player_ids]
    selected_players = db.session.execute(
    db.select(Player).where(Player.id.in_(player_ids))).scalars().all()
    for player in selected_players:
        print(player.name)
    return "Received players"
with app.app_context():
    '''
    creates any missing database tables based on my models.
    '''
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True)