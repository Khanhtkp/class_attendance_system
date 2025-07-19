let videoStream = null;
let intervalId = null;

document.querySelectorAll(".class-card").forEach(card => {
    card.addEventListener("click", () => {
        const className = card.dataset.class;
        fetch(`/get_class_data?class_name=${className}`)
            .then(res => res.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }

                const tableDiv = document.getElementById("student-table");
                let html = "<table border='1'><tr>";
                data.headers.forEach(h => html += `<th>${h}</th>`);
                html += "</tr>";
                data.students.forEach(row => {
                    html += "<tr>";
                    data.headers.forEach(h => html += `<td>${row[h]}</td>`);
                    html += "</tr>";
                });
                html += "</table>";
                tableDiv.innerHTML = html;

                document.getElementById("start-attendance").style.display = "block";
            });
    });
});

document.getElementById("start-attendance").addEventListener("click", () => {
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const ctx = canvas.getContext("2d");

    // Hi?n webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            videoStream = stream;

            // B?t ??u g?i frame liên t?c
            intervalId = setInterval(() => {
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                const imageData = canvas.toDataURL("image/jpeg");

                fetch("/process_frame", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ image: imageData })
                })
                .then(res => res.json())
                .then(data => {
                    document.getElementById("processed-img").src = data.image;
                });
            }, 1000);
        });
});
