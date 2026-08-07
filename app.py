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

players = [ {
        "name": "Danny",
        "athleticism": 7,
        "technical": 8,
        "football_iq": 9
    },  
    {
        "name": "Aden",
        "athleticism": 6,
        "technical": 8.5,
        "football_iq": 10
    } ]

class Player(db.Model):
    '''
    Database of players
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

        new_player = Player(
    name= player_name,
    athleticism=float(request.form["athleticism"]),
    technical=float(request.form["technical"]),
    football_iq=float(request.form["football_iq"])
)

        if player_name:
            db.session.add(new_player)
            db.session.commit()

        return redirect(url_for("home"))

    players = db.session.execute(db.select(Player)).scalars().all()

    return render_template(
        "index.html",
        players=players,
        player_count=len(players)
    )
with app.app_context():
    db.create_all()
if __name__ == "__main__":
    app.run(debug=True)