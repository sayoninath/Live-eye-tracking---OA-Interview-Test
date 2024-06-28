document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('eye-tracking-canvas');
    const ctx = canvas.getContext('2d');

    // update the video stream
    async function updateVideoStream() {
        try {
            const response = await fetch('/video_feed');
            const blob = await response.blob();
            const objectURL = URL.createObjectURL(blob);
            const video = document.getElementById('eye-tracking-video');
            video.src = objectURL;
        } catch (error) {
            console.error('Error fetching video stream:', error);
        }
    }

    setInterval(updateVideoStream, 500); // Update the video stream every 0.5 seconds

    function updateGazeDirection(x, y) {
        let gazeDirection = '';

        if (x < -50) {
            gazeDirection = 'Looking Left';
        } else if (x > 50) {
            gazeDirection = 'Looking Right';
        } else if (y < -50) {
            gazeDirection = 'Looking Up';
        } else if (y > 50) {
            gazeDirection = 'Looking Down';
        } else {
            gazeDirection = 'Looking Straight';
        }

        document.getElementById('gaze-direction').textContent = gazeDirection;
    }

    function updateGazeData() {
        fetch('/gaze_data')
            .then(response => response.json())
            .then(data => {
                const { x, y } = data;
                updateGazeDirection(x, y);
            })
            .catch(error => {
                console.error('Error fetching gaze data:', error);
            });
    }

    setInterval(updateGazeData, 500); // Update gaze data every 0.5 seconds

    function updateTimer() {
        let secondsLeft = 300;
        const timerElement = document.getElementById('time-remaining');

        const intervalId = setInterval(() => {
            const minutes = Math.floor(secondsLeft / 60);
            const seconds = secondsLeft % 60;
            timerElement.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

            if (secondsLeft <= 0) {
                clearInterval(intervalId);
            } else {
                secondsLeft--;
            }
        }, 1000);
    }

    updateTimer(); // 

    document.getElementById('submit-btn').addEventListener('click', function() {
        alert('MCQ Answers Submitted!');
    });
});
