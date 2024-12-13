import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from pix2text import Pix2Text

# Flask App
app = Flask(__name__)

# Folder Uploads
UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create Upload Folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Check Allowed File Extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route: Home Page
@app.route('/')
def index():
    return render_template('index.html')

# Route: Upload File and Process OCR
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Sử dụng Pix2Text để nhận diện công thức
            p2t = Pix2Text.from_config()
            equations = p2t.recognize_formula(filepath)

            # Hiển thị kết quả trên giao diện
            return render_template(
                'result.html',
                equations=equations,
                image_path=filename
            )
        except Exception as e:
            return render_template('error.html', error_message=str(e))

    # Nếu file không hợp lệ
    return redirect(url_for('index'))

# Route: Serve Uploaded Files
@app.route('/uploads/<filename>', endpoint='uploads')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Run the App
if __name__ == '__main__':
    app.run(debug=True)
