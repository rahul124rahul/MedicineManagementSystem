from flask import Flask
from config import Config
from models import db
from models.patient import Patient
from models.medicine import Medicine
from models.dose import Dose

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Create tables automatically
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Medicine Management System Backend Running"

if __name__ == "__main__":
    app.run(debug=True)