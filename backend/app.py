# #working code on local host
# import cv2
# import base64
# import eventlet
# from flask import Flask
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from eventlet import greenthread

# print("Starting the app...")  # Debugging print

# # Initialize Flask and SocketIO
# app = Flask(__name__)
# CORS(app)  # Enable CORS for Flask

# socketio = SocketIO(app, cors_allowed_origins="*")  # Use Flask-SocketIO and allow CORS

# print("App initialized...")  # Debugging print

# # Global flag and variables
# is_streaming = False
# camera = None

# # Function to capture and stream the video feed
# def capture_camera():
#     global is_streaming, camera

#     while True:
#         if is_streaming:
#             if camera is None or not camera.isOpened():
#                 # Initialize the camera capture when starting the stream
#                 print("Connecting to the camera...")
#                 camera = cv2.VideoCapture('rtsp://admin:Admin@123@192.168.1.64:554/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')
#                 if camera.isOpened():
#                     print("Successfully connected to the camera")
#                 else:
#                     print("Error: Unable to connect to the camera")
#                     continue

#             ret, frame = camera.read()
#             if not ret:
#                 print("Error: Unable to fetch frame from IP camera")
#                 continue

#             # Encode the frame as JPEG
#             _, buffer = cv2.imencode('.jpg', frame)

#             # Convert the frame to base64 string
#             frame_base64 = base64.b64encode(buffer).decode('utf-8')

#             # Emit the frame over the socket
#             socketio.emit('video_frame', frame_base64)
#             print("Frame emitted")
        
#         eventlet.sleep(0.03)  # Delay to control frame rate


# # API to take a snapshot
# @app.route('/take_snapshot', methods=['POST', 'OPTIONS'])
# def take_snapshot():
#     # Handle preflight requests
#     if request.method == "OPTIONS":
#         return _build_cors_preflight_response()
    
#     global camera
#     print("Snapshot request received")

#     if camera is not None and camera.isOpened():
#         ret, frame = camera.read()
#         if ret:
#             # Save snapshot
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             file_name = f"snapshot_{timestamp}.jpg"
#             snapshot_path = os.path.join('backend/snapshot', file_name)
#             cv2.imwrite(snapshot_path, frame)
#             print(f"Snapshot saved at {snapshot_path}")
#             return _corsify_actual_response(jsonify({"message": "Snapshot taken", "filename": file_name})), 200
#         else:
#             return _corsify_actual_response(jsonify({"error": "Failed to capture frame"})), 500
#     else:
#         return _corsify_actual_response(jsonify({"error": "Camera not available"})), 500

# # CORS handling functions
# def _build_cors_preflight_response():
#     response = jsonify({'status': 'OK'})
#     response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type")
#     response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
#     return response

# def _corsify_actual_response(response):
#     response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
#     return response


# # Event listener for client connection
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# # Event listener for "start_stream" event
# @socketio.on('start_stream')
# def handle_start_stream():
#     global is_streaming
#     is_streaming = True
#     print("Streaming started")

# # Event listener for "stop_stream" event
# @socketio.on('stop_stream')
# def handle_stop_stream():
#     global is_streaming, camera
#     is_streaming = False
#     print("Streaming stopped")

#     # Release the camera when stopping the stream
#     if camera is not None and camera.isOpened():
#         camera.release()
#         camera = None
#         print("Camera connection released")

# # Event listener for client disconnect
# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")

# # Flask route for root URL
# @app.route('/')
# def index():
#     print("Root URL accessed.")
#     return "Socket.IO server is running."


# # Run the camera capture in a separate thread
# greenthread.spawn(capture_camera)

# print("Running the app...")  # Debugging print

# # Start the server
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5002)
















#working code with ngrok
# import cv2
# import base64
# import eventlet
# from flask import Flask, render_template  # Added render_template to serve HTML
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from eventlet import greenthread

# print("Starting the app...")  # Debugging print

# # Initialize Flask and SocketIO
# app = Flask(__name__, static_folder="static", template_folder="templates")  # Updated to serve static and templates
# CORS(app)  # Enable CORS for Flask

# socketio = SocketIO(app, cors_allowed_origins="*")  # Use Flask-SocketIO and allow CORS

# print("App initialized...")  # Debugging print

# # Global flag and variables
# is_streaming = False
# camera = None

# # Function to capture and stream the video feed
# def capture_camera():
#     global is_streaming, camera

#     while True:
#         if is_streaming:
#             if camera is None or not camera.isOpened():
#                 # Initialize the camera capture when starting the stream
#                 print("Connecting to the camera...")
#                 camera = cv2.VideoCapture('rtsp://admin:Admin@123@192.168.1.64:554/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')
#                 if camera.isOpened():
#                     print("Successfully connected to the camera")
#                 else:
#                     print("Error: Unable to connect to the camera")
#                     continue

#             ret, frame = camera.read()
#             if not ret:
#                 print("Error: Unable to fetch frame from IP camera")
#                 continue

#             # Encode the frame as JPEG
#             # _, buffer = cv2.imencode('.jpg', frame)

#             # Convert the frame to base64 string
#             frame_base64 = base64.b64encode(frame).decode('utf-8')

#             # Emit the frame over the socket
#             socketio.emit('video_frame', frame_base64)
#             print("Frame emitted")
        
#         eventlet.sleep(0.03)  # Delay to control frame rate

# # Event listener for client connection
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# # Event listener for "start_stream" event
# @socketio.on('start_stream')
# def handle_start_stream():
#     global is_streaming
#     is_streaming = True
#     print("Streaming started")

# # Event listener for "stop_stream" event
# @socketio.on('stop_stream')
# def handle_stop_stream():
#     global is_streaming, camera
#     is_streaming = False
#     print("Streaming stopped")

#     # Release the camera when stopping the stream
#     if camera is not None and camera.isOpened():
#         camera.release()
#         camera = None
#         print("Camera connection released")

# # Event listener for client disconnect
# @socketio.on('disconnect')
# def handle_disconnect():
#     print("Client disconnected")

# # Flask route for serving the frontend
# @app.route('/')
# def index():
#     return render_template('index.html')  # Serve index.html

# # Run the camera capture in a separate thread
# greenthread.spawn(capture_camera)

# print("Running the app...")  # Debugging print

# # Start the server
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5002)


#ss
# import os
# import cv2
# import base64
# import eventlet
# from flask import Flask, jsonify, send_from_directory, render_template
# from flask_socketio import SocketIO
# from flask_cors import CORS
# from datetime import datetime

# # Path where snapshots will be stored
# SNAPSHOT_FOLDER = os.path.join(os.getcwd(), 'backend', 'snapshot')

# # Ensure snapshot folder exists
# if not os.path.exists(SNAPSHOT_FOLDER):
#     os.makedirs(SNAPSHOT_FOLDER)
#     print(f"Created snapshot folder at: {SNAPSHOT_FOLDER}")

# print("Starting the app...")

# app = Flask(__name__, static_folder='static', template_folder='templates')
# CORS(app)

# socketio = SocketIO(app, cors_allowed_origins="*")

# # Global variables
# is_streaming = False
# camera = None

# # Serve the index.html
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Function to capture and stream the video feed
# def capture_camera():
#     global is_streaming, camera

#     while True:
#         if is_streaming:
#             if camera is None or not camera.isOpened():
#                 print("Attempting to connect to the camera...")
#                 camera = cv2.VideoCapture('rtsp://admin:Admin@123@192.168.1.64:554/Streaming/Channels/101?transportmode=unicast&profile=Profile_1')

#                 # Check if the camera successfully opened
#                 if camera.isOpened():
#                     print("Successfully connected to the camera")
#                 else:
#                     print("Error: Unable to connect to the camera")
#                     eventlet.sleep(5)  # Retry connection after a delay
#                     continue

#             ret, frame = camera.read()
#             if not ret:
#                 print("Error: Unable to fetch frame from IP camera")
#                 continue

#             # Encode the frame as JPEG
#             _, buffer = cv2.imencode('.jpg', frame)

#             # Convert the frame to base64 string
#             frame_base64 = base64.b64encode(buffer).decode('utf-8')

#             # Emit the frame over the socket
#             socketio.emit('video_frame', frame_base64)
#             print("Frame emitted")
        
#         eventlet.sleep(0.03)  # Delay to control frame rate


# # API to take a snapshot
# @app.route('/take_snapshot', methods=['POST'])
# def take_snapshot():
#     global camera
#     print("Snapshot request received")  # Added this debug log

#     if camera is not None and camera.isOpened():
#         print("Camera is opened. Capturing frame...")
#         ret, frame = camera.read()
#         if ret:
#             # Save snapshot
#             timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#             file_name = f"snapshot_{timestamp}.jpg"
#             snapshot_path = os.path.join(SNAPSHOT_FOLDER, file_name)
#             print(f"Saving snapshot at {snapshot_path}")
            
#             cv2.imwrite(snapshot_path, frame)
#             print(f"Snapshot saved at {snapshot_path}")
#             return jsonify({"message": "Snapshot taken", "filename": file_name}), 200
#         else:
#             print("Error: Failed to capture frame from camera")
#             return jsonify({"error": "Failed to capture frame"}), 500
#     else:
#         print("Error: Camera not opened or streaming")
#         return jsonify({"error": "Camera not available"}), 500

# # Serve the snapshots
# @app.route('/snapshot/<filename>')
# def get_snapshot(filename):
#     return send_from_directory(SNAPSHOT_FOLDER, filename)

# # Handle client connection
# @socketio.on('connect')
# def handle_connect():
#     print("Client connected")

# @socketio.on('start_stream')
# def handle_start_stream():
#     global is_streaming
#     is_streaming = True
#     print("Streaming started")

# @socketio.on('stop_stream')
# def handle_stop_stream():
#     global is_streaming, camera
#     is_streaming = False
#     if camera is not None and camera.isOpened():
#         camera.release()
#         camera = None
#         print("Camera connection closed")

# # Test Route to Check API Connectivity
# @app.route('/test_snapshot', methods=['GET'])
# def test_snapshot():
#     print("Test snapshot route hit")
#     return jsonify({"message": "Test snapshot route working!"}), 200

# # Running the camera thread
# eventlet.greenthread.spawn(capture_camera)

# # Start the server
# if __name__ == '__main__':
#     socketio.run(app, host='0.0.0.0', port=5002)





import cv2
import base64
import os
from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from datetime import datetime
import eventlet
from flask import send_from_directory
app = Flask(__name__) 

socketio = SocketIO(app, cors_allowed_origins="*")  

is_streaming = False
camera = None


def capture_camera():
    global is_streaming, camera

    while True:
        if is_streaming:
            if camera is None or not camera.isOpened():
                print("Connecting to the camera...")
                camera = cv2.VideoCapture('your_rtsp_link')
                if camera.isOpened():
                    print("Successfully connected to the camera")
                else:
                    print("Error: Unable to connect to the camera")
                    continue

            ret, frame = camera.read()
            if not ret:
                print("Error: Unable to fetch frame from IP camera")
                continue

            _, buffer = cv2.imencode('.jpg', frame)

            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            socketio.emit('video_frame', frame_base64)
            # print("Frame emitted")
        
        eventlet.sleep(0.03) 

@app.route('/snapshot/<filename>')
def get_snapshot(filename):
    return send_from_directory('backend/snapshot', filename)
@app.route('/take_snapshot', methods=['POST', 'OPTIONS'])
def take_snapshot():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

    global camera
    print("Snapshot request received")

    if camera is not None and camera.isOpened():
        ret, frame = camera.read()
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name = f"snapshot_{timestamp}.jpg"
            snapshot_path = os.path.join('backend/snapshot', file_name)
            cv2.imwrite(snapshot_path, frame)
            print(f"Snapshot saved at {snapshot_path}")
            return _corsify_actual_response(jsonify({"message": "Snapshot taken", "filename": file_name})), 200
        else:
            return _corsify_actual_response(jsonify({"error": "Failed to capture frame"})), 500
    else:
        return _corsify_actual_response(jsonify({"error": "Camera not available"})), 500

def _build_cors_preflight_response():
    response = jsonify({'status': 'OK'})
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
    return response


@socketio.on('connect')
def handle_connect():
    print("Client connected")

@socketio.on('start_stream')
def handle_start_stream():
    global is_streaming
    is_streaming = True
    print("Streaming started")

@socketio.on('stop_stream')
def handle_stop_stream():
    global is_streaming, camera
    is_streaming = False
    print("Streaming stopped")

    if camera is not None and camera.isOpened():
        camera.release()
        camera = None
        print("Camera connection released")

@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected")

@app.route('/')
def index():
    return "Socket.IO server is running."


eventlet.greenthread.spawn(capture_camera)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002)
