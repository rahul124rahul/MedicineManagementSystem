from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ==============================
# DATABASE CONFIGURATION
# ==============================
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Rahul123@localhost/medicine_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ==============================
# MODELS
# ==============================

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    medicines = db.relationship("Medicine", backref="patient", cascade="all, delete", lazy=True)


class Medicine(db.Model):
    __tablename__ = "medicines"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=True)

    doses = db.relationship("Dose", backref="medicine", cascade="all, delete", lazy=True)


class Dose(db.Model):
    __tablename__ = "doses"

    id = db.Column(db.Integer, primary_key=True)
    dosage_amount = db.Column(db.String(100), nullable=False)
    schedule = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.String(50), nullable=False)
    end_date = db.Column(db.String(50), nullable=False)

    medicine_id = db.Column(db.Integer, db.ForeignKey("medicines.id"), nullable=False)


# ==============================
# HOME ROUTE
# ==============================

@app.route("/")
def home():
    return render_template("layout.html")


# ==============================
# PATIENT ROUTES
# ==============================

@app.route("/patients")
def patients_page():
    patients = Patient.query.all()
    return render_template("patients.html", patients=patients)


@app.route("/add_patient", methods=["POST"])
def add_patient():

    name = request.form.get("name")
    age = request.form.get("age")
    gender = request.form.get("gender")

    if not name or not age or not gender:
        return "Required fields missing!", 400

    patient = Patient(
        name=name,
        age=int(age),
        gender=gender
    )

    db.session.add(patient)
    db.session.commit()

    # OPTIONAL MEDICINE
    medicine_name = request.form.get("medicine_name")
    description = request.form.get("description")

    if medicine_name:
        medicine = Medicine(
            name=medicine_name,
            description=description,
            patient_id=patient.id
        )
        db.session.add(medicine)
        db.session.commit()

        # OPTIONAL DOSE
        dosage_amount = request.form.get("dosage_amount")
        schedule = request.form.get("schedule")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")

        if dosage_amount and schedule and start_date and end_date:
            dose = Dose(
                dosage_amount=dosage_amount,
                schedule=schedule,
                start_date=start_date,
                end_date=end_date,
                medicine_id=medicine.id
            )
            db.session.add(dose)
            db.session.commit()

    return redirect("/patients")


@app.route("/patient/<int:id>")
def patient_details(id):
    patient = Patient.query.get_or_404(id)
    return render_template("patient_details.html", patient=patient)


@app.route("/edit_patient/<int:id>", methods=["GET", "POST"])
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")

        if not name or not age or not gender:
            return "All fields required!", 400

        patient.name = name
        patient.age = int(age)
        patient.gender = gender

        db.session.commit()
        return redirect("/patients")

    return render_template("edit_patient.html", patient=patient)

# ==============================
# MEDICINE ROUTES
# ==============================

@app.route("/medicines")
def medicines_page():
    medicines = Medicine.query.all()
    patients = Patient.query.all()
    return render_template("medicines.html", medicines=medicines, patients=patients)


@app.route("/add_medicine", methods=["POST"])
def add_medicine():

    name = request.form.get("name")
    description = request.form.get("description")
    patient_id = request.form.get("patient_id")

    if not name:
        return "Medicine name required!", 400

    medicine = Medicine(
        name=name,
        description=description,
        patient_id=int(patient_id) if patient_id else None
    )

    db.session.add(medicine)
    db.session.commit()

    return redirect("/medicines")


@app.route("/add_medicine_to_patient/<int:patient_id>", methods=["POST"])
def add_medicine_to_patient(patient_id):

    name = request.form.get("name")
    description = request.form.get("description")

    medicine = Medicine(
        name=name,
        description=description,
        patient_id=patient_id
    )

    db.session.add(medicine)
    db.session.commit()

    return redirect(f"/patient/{patient_id}")


# ==============================
# DOSE ROUTES
# ==============================

@app.route("/add_dose/<int:medicine_id>", methods=["POST"])
def add_dose(medicine_id):

    medicine = Medicine.query.get_or_404(medicine_id)

    dosage_amount = request.form.get("dosage_amount")
    schedule = request.form.get("schedule")
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")

    if not dosage_amount or not schedule or not start_date or not end_date:
        return "All dose fields required!", 400

    dose = Dose(
        dosage_amount=dosage_amount,
        schedule=schedule,
        start_date=start_date,
        end_date=end_date,
        medicine_id=medicine.id
    )

    db.session.add(dose)
    db.session.commit()

    return redirect(f"/patient/{medicine.patient_id}")


# ==============================
# DATABASE INIT (RUN ONCE)
# ==============================

with app.app_context():
    db.create_all()


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    app.run(debug=True)