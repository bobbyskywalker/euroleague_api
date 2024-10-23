from flask import Flask, render_template, jsonify, request
from get_players import retrieve_players

app = Flask(__name__)
@app.route("/players/<int:season>", methods = ['GET'])
def get_players(season):
    players_json = retrieve_players(season)
    if players_json == '[]':
        return '404 Not Found: The requested URL was not found on the server.'
    return players_json

if __name__ == '__main__':
    app.run(debug=True)