document.addEventListener("DOMContentLoaded", function () {
    if (document.getElementById("patientList")) {
        loadPatients();
    }
    if (document.getElementById("medicineList")) {
        loadMedicines();
    }
});

/* ================= PATIENTS ================= */

async function loadPatients() {
    const res = await fetch("/patients");
    const data = await res.json();

    let html = "";
    data.forEach(p => {
        html += `
        <div class="card">
            <b>${p.name}</b> (${p.age}) - ${p.gender}
            <button onclick="showPatient(${p.id})">Show</button>
        </div>`;
    });

    document.getElementById("patientList").innerHTML = html;
}

async function addPatient() {
    const name = document.getElementById("pname").value;
    const age = document.getElementById("page").value;
    const gender = document.getElementById("pgender").value;
    const contact = document.getElementById("pcontact").value;

    await fetch("/patients", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, age, gender, contact})
    });

    loadPatients();
}

async function showPatient(id) {
    const res = await fetch(`/patients/${id}`);
    const data = await res.json();

    let html = `
    <div class="card detail-box">
        <h3>${data.name} Details</h3>
        <p><b>Age:</b> ${data.age}</p>
        <p><b>Gender:</b> ${data.gender}</p>
        <p><b>Contact:</b> ${data.contact}</p>
    `;

    data.medicines.forEach(m => {
        html += `
        <div class="card">
            <b>${m.name}</b> - ${m.description}
            <button onclick="addDose(${m.id}, ${id})">Add Dose</button>
            <ul>`;
        m.doses.forEach(d => {
            html += `<li>${d.time} - ${d.quantity}</li>`;
        });
        html += `</ul></div>`;
    });

    html += "</div>";

    document.getElementById("patientDetails").innerHTML = html;
}


/* ================= MEDICINES ================= */

async function loadMedicines() {
    const pres = await fetch("/patients");
    const patients = await pres.json();

    let dropdown = `<option value="">-- No Patient --</option>`;
    patients.forEach(p => {
        dropdown += `<option value="${p.id}">${p.name}</option>`;
    });

    document.getElementById("patientDropdown").innerHTML = dropdown;

    const mres = await fetch("/medicines");
    const medicines = await mres.json();

    let html = "";
    medicines.forEach(m => {
        html += `
        <div class="card">
            <b>${m.name}</b> - ${m.description}
            <p><b>Assigned To:</b> ${m.patient_name}</p>
            <button onclick="assignMedicine(${m.id})">Assign</button>
        </div>`;
    });

    document.getElementById("medicineList").innerHTML = html;
}

async function assignMedicine(medicine_id) {
    const patient_id = prompt("Enter Patient ID to assign:");

    if (!patient_id) return;

    await fetch("/assign-medicine", {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({medicine_id, patient_id})
    });

    alert("Medicine Assigned");
    loadMedicines();
}

async function addMedicine() {
    const name = document.getElementById("mname").value;
    const description = document.getElementById("mdesc").value;
    const patient_id = document.getElementById("patientDropdown").value;

    await fetch("/medicines", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name, description, patient_id})
    });

    loadMedicines();
}

async function addDose(medicine_id, patient_id) {
    const time = prompt("Enter Time (Morning/Night):");
    const quantity = prompt("Enter Quantity:");

    await fetch("/doses", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({time, quantity, medicine_id})
    });

    alert("Dose Added");
    showPatient(patient_id); // 🔥 refresh
}