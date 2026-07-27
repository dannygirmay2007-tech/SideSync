from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
players = ["Danny", "Aden", "Yafiet", "Player 4"]
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        player_name = request.form["player_name"].strip()

        if player_name:
            players.append(player_name)
        return redirect(url_for("home"))
    return render_template("index.html", players = players, player_count = len(players))
if __name__ == "__main__":
    app.run(debug=True)