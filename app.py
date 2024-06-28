from flask import Flask, render_template, Response, redirect, url_for, request
from eye_tracker_library import EyeTracker

app = Flask(__name__)
eye_tracker = EyeTracker()

successful_submission = False  

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    while True:
        frame = eye_tracker.get_frame_with_detections()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/submit_test', methods=['POST'])
def submit_test():
    global successful_submission  # Make the variable accessible
    #handle form submission and check for successful submission
    successful_submission = True 
    return redirect(url_for('submit_confirmation'))

@app.route('/submit_confirmation')
def submit_confirmation():
    return render_template('submit.html')

if __name__ == "__main__":
    app.run(debug=True)
