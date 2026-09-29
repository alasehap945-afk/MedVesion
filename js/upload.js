const imageInput = document.getElementById("imageInput");
const imagePreview = document.getElementById("imagePreview");
const previewContainer = document.getElementById("previewContainer");
const fileName = document.getElementById("fileName");
const processBtn = document.getElementById("processBtn");


imageInput.addEventListener("change", function () {

    const file = this.files[0];

    if (!file) {
        return;
    }

    const imageURL = URL.createObjectURL(file);

    imagePreview.src = imageURL;

    fileName.textContent = file.name;

    previewContainer.style.display = "block";
});


processBtn.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        alert("Please choose an image first.");
        return;
    }

    processBtn.disabled = true;

    processBtn.innerHTML = `
        Processing...
        <i class="bi bi-hourglass-split"></i>
    `;


    const formData = new FormData();

    formData.append("image", file);


    try {

        const response = await fetch("/process", {
            method: "POST",
            body: formData
        });


        const data = await response.json();


        if (!response.ok) {
            throw new Error(data.error || "Processing failed.");
        }


        window.location.href = data.redirect;


    } catch (error) {

        alert(error.message);

        processBtn.disabled = false;

        processBtn.innerHTML = `
            Process Image
            <i class="bi bi-arrow-right"></i>
        `;
    }
});