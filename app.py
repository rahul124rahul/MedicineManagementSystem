from flask import Flask, request, jsonify
from config import Config
from models import db
from models.patient import Patient
from models.medicine import Medicine
from models.dose import Dose

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# ==============================
# PATIENT APIs
# ==============================

# Create Patient
@app.route("/patients", methods=["POST"])
def create_patient():
    data = request.json

    new_patient = Patient(
        name=data["name"],
        age=data["age"],
        gender=data["gender"],
        contact=data["contact"]
    )

    db.session.add(new_patient)
    db.session.commit()

    return jsonify({"message": "Patient created successfully"}), 201


# Get All Patients
@app.route("/patients", methods=["GET"])
def get_patients():
    patients = Patient.query.all()

    result = []
    for p in patients:
        result.append({
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "contact": p.contact
        })

    return jsonify(result)


# Get Single Patient with Medicines & Doses
@app.route("/patients/<int:id>", methods=["GET"])
def get_patient(id):
    patient = Patient.query.get_or_404(id)

    medicines_list = []
    for med in patient.medicines:
        doses_list = []
        for d in med.doses:
            doses_list.append({
                "id": d.id,
                "time": d.time,
                "quantity": d.quantity
            })

        medicines_list.append({
            "id": med.id,
            "name": med.name,
            "description": med.description,
            "doses": doses_list
        })

    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "gender": patient.gender,
        "contact": patient.contact,
        "medicines": medicines_list
    })


# Update Patient
@app.route("/patients/<int:id>", methods=["PUT"])
def update_patient(id):
    patient = Patient.query.get_or_404(id)
    data = request.json

    patient.name = data["name"]
    patient.age = data["age"]
    patient.gender = data["gender"]
    patient.contact = data["contact"]

    db.session.commit()

    return jsonify({"message": "Patient updated successfully"})


# Delete Patient
@app.route("/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):
    patient = Patient.query.get_or_404(id)

    db.session.delete(patient)
    db.session.commit()

    return jsonify({"message": "Patient deleted successfully"})


# ==============================
# MEDICINE APIs
# ==============================

# Add Medicine
@app.route("/medicines", methods=["POST"])
def create_medicine():
    data = request.json

    new_medicine = Medicine(
        name=data["name"],
        description=data["description"],
        patient_id=data["patient_id"]
    )

    db.session.add(new_medicine)
    db.session.commit()

    return jsonify({"message": "Medicine added successfully"}), 201


# Update Medicine
@app.route("/medicines/<int:id>", methods=["PUT"])
def update_medicine(id):
    medicine = Medicine.query.get_or_404(id)
    data = request.json

    medicine.name = data["name"]
    medicine.description = data["description"]

    db.session.commit()

    return jsonify({"message": "Medicine updated successfully"})


# Delete Medicine
@app.route("/medicines/<int:id>", methods=["DELETE"])
def delete_medicine(id):
    medicine = Medicine.query.get_or_404(id)

    db.session.delete(medicine)
    db.session.commit()

    return jsonify({"message": "Medicine deleted successfully"})


# ==============================
# DOSE APIs
# ==============================

# Add Dose
@app.route("/doses", methods=["POST"])
def create_dose():
    data = request.json

    new_dose = Dose(
        time=data["time"],
        quantity=data["quantity"],
        medicine_id=data["medicine_id"]
    )

    db.session.add(new_dose)
    db.session.commit()

    return jsonify({"message": "Dose added successfully"}), 201


# Update Dose
@app.route("/doses/<int:id>", methods=["PUT"])
def update_dose(id):
    dose = Dose.query.get_or_404(id)
    data = request.json

    dose.time = data["time"]
    dose.quantity = data["quantity"]

    db.session.commit()

    return jsonify({"message": "Dose updated successfully"})


# Delete Dose
@app.route("/doses/<int:id>", methods=["DELETE"])
def delete_dose(id):
    dose = Dose.query.get_or_404(id)

    db.session.delete(dose)
    db.session.commit()

    return jsonify({"message": "Dose deleted successfully"})


# ==============================

if __name__ == "__main__":
    app.run(debug=True)