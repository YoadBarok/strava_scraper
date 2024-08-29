from flask import Flask
from dotenv import load_dotenv
from blueprints.plotting import plotting_bp
from blueprints.auth import auth_bp
from blueprints.activities import activities_bp

load_dotenv()

app = Flask(__name__)

app.register_blueprint(plotting_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(activities_bp)


if __name__ == "__main__":
    app.run(port=8080, debug=True)
