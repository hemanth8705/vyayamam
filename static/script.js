function sendCommand(command) {
    fetch(`/control/${command}`)
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById("status");
            if (data.status) {
                statusElement.textContent = `Status: ${data.status}`;
            } else if (data.error) {
                statusElement.textContent = `Error: ${data.error}`;
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
}

// Additional controls for the video player
const videoPlayer = document.getElementById("video-player");

videoPlayer.onplay = function() {
    sendCommand('play');
};

videoPlayer.onpause = function() {
    sendCommand('pause');
};

videoPlayer.onended = function() {
    sendCommand('stop');
};
