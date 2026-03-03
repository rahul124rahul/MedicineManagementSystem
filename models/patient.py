from . import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    contact = db.Column(db.String(20), unique=True, nullable=False)

    # One-to-Many relationship
    medicines = db.relationship(
        "Medicine",
        backref="patient",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Patient {self.name}>"