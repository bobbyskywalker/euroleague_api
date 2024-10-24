from flask import Flask
from flask import jsonify

from routes.player_requests import players_bp
from routes.team_requests import teams_bp

db_path = "/home/olek/Desktop/my_projects/python_projects/euroleague_project/euroleague_db_creator/euroleague.db"

app = Flask(__name__)

app.register_blueprint(players_bp)
app.register_blueprint(teams_bp)

if __name__ == "__main__":
    app.run(debug=True)
