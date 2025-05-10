from flask import Flask
from flask_cors import CORS
import os

from bug_handling.choose_db import get_db_config
_ = get_db_config()

app = Flask(__name__)
CORS(app)

from app.controller.controller_athletes import athlete_routes
from app.controller.controller_teams import team_routes
from app.controller.controller_analytics import analytics_routes
from app.controller.controller_exercises import exercise_routes
from app.controller.controller_relationships import relationships_routes
from app.controller.controller_auth import auth_routes

app.register_blueprint(athlete_routes)
app.register_blueprint(team_routes)
app.register_blueprint(analytics_routes)
app.register_blueprint(relationships_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(exercise_routes)


@app.route("/")
def index():
    return "Welcome to the SportsTracker API for DB team PHGA. Keep doing your thing on Postman."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
