from flask import Flask, request, jsonify, render_template
from io import BytesIO
from PIL import Image
import base64

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def string_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def binary_to_string(binary):
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

@app.route('/encode', methods=['POST'])
def encode_message():
    file = request.files['image']
    message = request.form['message']

    img = Image.open(file.stream)
    img = img.convert('RGB')  # Force convert to RGB

    binary_message = string_to_binary(message) + '1111111111111110'  # End marker
    pixels = img.load()
    data_index = 0

    for y in range(img.height):
        for x in range(img.width):
            if data_index < len(binary_message):
                r, g, b = pixels[x, y]
                r = (r & ~1) | int(binary_message[data_index])
                data_index += 1
                if data_index < len(binary_message):
                    g = (g & ~1) | int(binary_message[data_index])
                    data_index += 1
                if data_index < len(binary_message):
                    b = (b & ~1) | int(binary_message[data_index])
                    data_index += 1
                pixels[x, y] = (r, g, b)

    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    encoded_image = base64.b64encode(img_io.read()).decode('utf-8')

    return jsonify({"encoded_image": encoded_image})

@app.route('/decode', methods=['POST'])
def decode_message():
    file = request.files['image']
    img = Image.open(file.stream)
    img = img.convert('RGB')

    binary_data = ''
    pixels = img.load()

    delimiter = '1111111111111110'
    
    found = False

    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]
            for color in (r, g, b):
                binary_data += str(color & 1)
                if binary_data.endswith(delimiter):
                    found = True
                    break
            if found:
                break
        if found:
            break

    if found:
        message_binary = binary_data[:-len(delimiter)]  # Remove delimiter bits
        decoded_message = binary_to_string(message_binary)
        return jsonify({"message": decoded_message})
    else:
        return jsonify({"message": "No hidden message found!"})

if __name__ == '__main__':
    app.run(debug=True)