from models import db

class Dose(db.Model):
    __tablename__ = "doses"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50))
    quantity = db.Column(db.String(50))

    medicine_id = db.Column(
        db.Integer,
        db.ForeignKey("medicines.id"),
        nullable=False
    )