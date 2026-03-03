// ================= PATIENT FORM =================

const patientForm = document.getElementById("patientForm");

if (patientForm) {
    patientForm.addEventListener("submit", function(e) {
        e.preventDefault();

        fetch("/patients", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: document.getElementById("name").value,
                age: document.getElementById("age").value,
                gender: document.getElementById("gender").value,
                contact: document.getElementById("contact").value
            })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
            loadPatients();
        });
    });
}

// ================= LOAD PATIENTS =================

function loadPatients() {
    fetch("/patients")
        .then(res => res.json())
        .then(data => {
            const tbody = document.querySelector("#patientsTable tbody");
            tbody.innerHTML = "";

            data.forEach(patient => {
                tbody.innerHTML += `
                    <tr>
                        <td>${patient.id}</td>
                        <td>${patient.name}</td>
                        <td>${patient.age}</td>
                        <td>${patient.gender}</td>
                        <td>${patient.contact}</td>
                    </tr>
                `;
            });
        });
}

// Load on page load
if (document.getElementById("patientsTable")) {
    loadPatients();
}


// ================= MEDICINE FORM =================

const medicineForm = document.getElementById("medicineForm");

if (medicineForm) {
    medicineForm.addEventListener("submit", function(e) {
        e.preventDefault();

        fetch("/medicines", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: document.getElementById("medName").value,
                description: document.getElementById("description").value,
                patient_id: document.getElementById("patientId").value
            })
        })
        .then(res => res.json())
        .then(data => {
            alert(data.message);
        });
    });
}