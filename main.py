from flask import Flask, render_template, Response, jsonify, request
from flask import url_for
import os
import cv2
from GenerateFrames import GenerateFrames
from werkzeug.utils import secure_filename
from CartoonFrames import cartoon

app = Flask(__name__)
generate_frames = GenerateFrames()

@app.route("/")
def render_root():
    return render_template("index.html")

@app.route("/RawVideo")
def raw_video():
    return Response(generate_frames.generate_frame("RawVideo"), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/CartoonVideo")
def cartoon_video():
    return Response(generate_frames.generate_frame("Cartoon"), mimetype="multipart/x-mixed-replace; boundary=frame")

upload_folder = os.path.join('static', 'cartoonized')
 
app.config['UPLOAD'] = upload_folder

@app.route('/cartoonize', methods=['POST'])
def cartoonize():
    try:
        # Check for image in the request
        if 'image' not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Secure the filename
        filename = secure_filename(file.filename)

        # Save the uploaded file
        save_path = os.path.join(app.config['UPLOAD'], filename)
        file.save(save_path)

        # Apply cartoonization (assuming `cartoon` takes a file path and returns the processed image)
        cartoonized_image = cartoon(save_path)  # Process the saved image with your cartoon function
        
        # Save the cartoonized image
        cartoonized_save_path = os.path.join(app.config['UPLOAD'], f'cartoon_{filename}')
        cv2.imwrite(cartoonized_save_path, cartoonized_image)  # Save the cartoonized image to the static folder

        # Generate the URL for the cartoonized image
        img_url = url_for('static', filename=f'cartoonized/cartoon_{filename}')
        return jsonify({"image_url": img_url}), 200

    except Exception as e:
        app.logger.error(f"Error in cartoonize: {e}")
        return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run()