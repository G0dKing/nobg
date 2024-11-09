from flask import Flask, render_template, request, redirect, url_for, send_file
from PIL import Image
import io
import os
import rembg

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def remove_background(image_data):
    output_data = rembg.remove(image_data)
    return output_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    input_data = file.read()
    processed_image_data = remove_background(input_data)

    processed_image = Image.open(io.BytesIO(processed_image_data))
    img_io = io.BytesIO()
    processed_image.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='nobg.png')

if __name__ == '__main__':
    app.run(debug=True)