from flask import Flask, render_template

app = Flask(__name__)
@app.route("/")
def home():
    players = ["Danny", "Aden", "Yafiet", "Player 4"]
    return render_template("index.html", players = players, player_count = len(players))
if __name__ == "__main__":
    app.run(debug=True)