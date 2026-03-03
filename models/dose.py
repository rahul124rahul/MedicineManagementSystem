from . import db

class Dose(db.Model):
    __tablename__ = "doses"

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.String(50), nullable=False)

    # Foreign Key to Medicine
    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)

    def __repr__(self):
        return f"<Dose {self.time} - {self.quantity}>"