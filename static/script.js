document.addEventListener('DOMContentLoaded', function() {
    document.getElementById("generateAudioButton").addEventListener("click", function () {
        console.log("Button clicked!"); // Check if this is printed
        const text = document.getElementById("textInput").value.trim();
        
        if (!text) {
            alert("Please enter some text!");
            return;
        }

        fetch("/generate_audio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || "Failed to generate audio");
                });
            }
        })
        .then(blob => {
            const audioUrl = URL.createObjectURL(blob);
            const audio = new Audio(audioUrl);
            audio.play();
        })
        .catch(error => {
            console.error("Error:", error);
            alert(error.message);
        });
    });
});