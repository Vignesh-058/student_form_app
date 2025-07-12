async function handleFormSubmit(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const age = document.getElementById("age").value;
    const gender = document.getElementById("male").checked ? "Male" : document.getElementById("female").checked ? "Female" : "";
    const course = document.getElementById("course").value;
    const email = document.getElementById("email").value;

    if (!name || !age || !gender || !email) {
        alert("Please fill in all required fields.");
        return;
    }

    const data = { name, age, gender, course, email };

    try {
        const response = await fetch("/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Data saved successfully!");

            const table = document.getElementById("two");
            const newRow = table.insertRow(-1);

            newRow.innerHTML = `
                <td>${name}</td>
                <td>${age}</td>
                <td>${gender}</td>
                <td>${course}</td>
                <td>${email}</td>
                <td><button onclick="deleteRow(this)">Delete</button></td>
            `;
        } else {
            alert("Failed to save data to server.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong.");
    }
}

function deleteRow(button) {
    const row = button.parentElement.parentElement;
    row.remove();
}
