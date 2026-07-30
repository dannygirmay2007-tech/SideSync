from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
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
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        player_name = request.form["player_name"].strip()

        new_player = {
            "name": player_name
        }

        rating_fields = [
            "athleticism",
            "technical",
            "football_iq"
        ]

        for field in rating_fields:
            new_player[field] = float(request.form[field])

        if player_name:
            players.append(new_player)

        return redirect(url_for("home"))

    return render_template(
        "index.html",
        players=players,
        player_count=len(players)
    )
if __name__ == "__main__":
    app.run(debug=True)