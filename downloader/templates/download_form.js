let selectedAction = ""; // To store the selected action value

function setActionValue(event) {
    selectedAction = event.target.value; // Capture the value of the clicked button
    console.log("Selected Action:", selectedAction);

    // Show/hide containers
    const previewContainer = document.getElementById("preview-container");
    const transcriptContainer = document.getElementById("transcript-container");

    if (selectedAction === "download") {
        previewContainer.style.display = "block";
        transcriptContainer.style.display = "none";
    } else if (selectedAction === "transcript") {
        previewContainer.style.display = "none";
        transcriptContainer.style.display = "block";
    }
}

async function submitForm(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const actionUrl = form.getAttribute("action");

    try {
        const response = await fetch(actionUrl, {
            method: form.getAttribute("method") || "POST",
            body: formData,
            headers: {
                "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Data:", data);
        
        if (data.status === "success") {
            // Update video details
            document.getElementById("video-title").textContent = data.title;
            document.getElementById("video-views").textContent = `Views: ${data.views}`;
            document.getElementById("video-duration").textContent = `Duration: ${data.duration} seconds`;
            document.getElementById("video-thumbnail").src = data.thumbnail;
            document.getElementById("video-thumbnail").style.display = "block";
            document.getElementById("video-source").src = data.file;
            document.getElementById("video-preview").style.display = "block";
            document.getElementById("video-preview").load();
            document.getElementById("video-controls").style.display = "block";

            // Add full video to version dropdown
            const videoVersionSelect = document.getElementById("video-version");
            videoVersionSelect.innerHTML = `<option value="${data.file}">Full Video</option>`;
        } else {
            console.error("Error:", data.message);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

function changeVideoVersion() {
    const selectedVersion = document.getElementById("video-version").value;
    const videoElement = document.getElementById("video-preview");
    videoElement.querySelector("source").src = selectedVersion;
    videoElement.load();
}

async function createTrimmedVideo() {
    const trimStart = document.getElementById("trim-start").value;
    const trimEnd = document.getElementById("trim-end").value;
    const videoSource = document.getElementById("video-version").value;

    const payload = {
        file: videoSource,
        start: trimStart,
        end: trimEnd,
    };

    try {
        const response = await fetch("/create-trimmed-video/", {
            method: "POST",
            body: JSON.stringify(payload),
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.status === "success") {
            // Add the new trimmed video to the dropdown
            const videoVersionSelect = document.getElementById("video-version");
            const option = document.createElement("option");
            option.value = data.file;
            option.textContent = `Trimmed (${trimStart}-${trimEnd})`;
            videoVersionSelect.appendChild(option);

            alert("Trimmed video created successfully!");
        } else {
            console.error("Error:", data.message);
        }
    } catch (error) {
        console.error("Error creating trimmed video:", error);
    }
}

function adjustAspectRatio() {
    const videoElement = document.getElementById("video-preview");
    const aspectRatio = document.getElementById("aspect-ratio").value;
    const [width, height] = aspectRatio.split(":").map(Number);
    const container = videoElement.parentNode;

    const containerWidth = container.offsetWidth;
    const containerHeight = (containerWidth * height) / width;

    videoElement.style.width = `${containerWidth}px`;
    videoElement.style.height = `${containerHeight}px`;
}

function saveTrimmedVideo() {
    const videoElement = document.getElementById("video-preview");
    const aspectRatio = document.getElementById("aspect-ratio").value;

    const [width, height] = aspectRatio.split(":").map(Number);

    const payload = {
        file: videoElement.querySelector("source").src,
        aspect_ratio: aspectRatio,
    };

    fetch("/save-trimmed-video/", {
        method: "POST",
        body: JSON.stringify(payload),
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
        },
    })
        .then((response) => response.json())
        .then((data) => {
            alert("Video saved successfully!");
        })
        .catch((error) => {
            console.error("Error saving video:", error);
        });
}

function recordVideoTime() {
    const videoElement = document.getElementById("video-preview");
    const currentTime = videoElement.currentTime;
    document.getElementById("recorded-time").textContent = `Recorded Time: ${currentTime.toFixed(2)} seconds`;
}

function downloadTranscript() {
    const transcriptContent = document.getElementById("transcript-content").innerText;
    const blob = new Blob([transcriptContent], { type: "text/plain" });
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "transcript.txt";
    a.click();

    URL.revokeObjectURL(url);
}
