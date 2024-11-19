from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from PIL import Image
import io
import base64

API_KEY = 'AIzaSyAV3ADdthFgsuPQoj07Yr5yy8r-BJ7TlTo'
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)
CORS(app)

@app.route('/describe', methods=['POST'])
def describe_arrival():
    # Get the image data from the request
    data = request.get_json()
    image_data = data['image']  # This is the base64 string
   
    # Decode the base64 string
    image_data = image_data.split(',')[1]  # Remove the metadata part
    image_bytes = base64.b64decode(image_data)
    pil_image = Image.open(io.BytesIO(image_bytes))
     # Create a new image with a white background
    white_background = Image.new("RGB", pil_image.size, (255, 255, 255))  # Create a white background
    white_background.paste(pil_image, (0, 0), pil_image)  # Paste the original image onto the white background

    # Save the image to a file
    white_background.save('output_image.png')  # Save the image as a PNG file
   
   
    # Update the prompt for OCR
    response = model.generate_content([f"Please perform OCR on this image and extract all visible numbers. just display the numbers near by near without seperating each other",
                                        white_background],
                                        generation_config=genai.types.GenerationConfig(
                                            temperature=0.5
                                        ))
    print(response)
    return jsonify({'text': response.text, 'image_path': 'output_image.png'})

if __name__ == '__main__':
    app.run(debug=True)