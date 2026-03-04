from models import db

class Medicine(db.Model):
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    patient_id = db.Column(
        db.Integer,
        db.ForeignKey("patients.id"),
        nullable=True
    )

    doses = db.relationship(
        "Dose",
        backref="medicine",
        cascade="all, delete-orphan"
    )