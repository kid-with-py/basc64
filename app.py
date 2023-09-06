from flask import Flask, render_template, request, jsonify
import cv2
import base64
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        # Check if an image file is in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        file = request.files['image']

        # Read the uploaded image using OpenCV
        nparr = np.fromstring(file.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert the image to Base64 format
        _, buffer = cv2.imencode('.jpg', img)
        base64_image = base64.b64encode(buffer).decode()
        
        # convert the basc64 image to JPEG
        image_data = base64.b64decode(base64_image)
        output_image_path = "output_image.jpg"
        with open(output_image_path, "wb") as image_file:
            image_file.write(image_data)
        print(f"Image saved to {output_image_path}")    

        # return jsonify({'base64_image': base64_image})
        return base64_image 
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    


if __name__ == '__main__':
    app.run(debug=True)
