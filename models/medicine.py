from . import db

class Medicine(db.Model):
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Foreign Key to Patient
    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)

    # One-to-Many with Dose
    doses = db.relationship(
        "Dose",
        backref="medicine",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Medicine {self.name}>"