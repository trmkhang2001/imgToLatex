import os
import pytesseract
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image

# Flask App
app = Flask(__name__)

# Folder Uploads
UPLOAD_FOLDER = os.path.abspath('uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Path to Tesseract-OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Debug: File Path
        print(f"File saved at: {filepath}")

        # Open Image and Extract Text with Tesseract
        image = Image.open(filepath)
        config = r'--psm 6'  # Use "PSM 6" for a single block of text (adjustable)
        text = pytesseract.image_to_string(image, config=config)

        # Clean the OCR Output and Prepare LaTeX (Optional Processing)
        latex_content = text  # If necessary, preprocess the text here

        # Render the Result Page
        return render_template(
            'result.html',
            text=text,
            image_path=filename,
            latex_content=latex_content
        )

    return redirect(url_for('index'))

# Route: Serve Uploaded Files
@app.route('/uploads/<filename>', endpoint='uploads')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Run the App
if __name__ == '__main__':
    app.run(debug=True)
