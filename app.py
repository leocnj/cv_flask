#
# based on https://stackoverflow.com/questions/11262518/how-to-pass-uploaded-image-to-template-html-in-flask
# - simple form to upload images
# - redirect to uploaded_file to show image
#
#
import os

from flask import Flask, render_template, request, send_from_directory, redirect, url_for

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.debug = True


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(f)
    return redirect(url_for('uploaded_file', filename=file.filename))


@app.route('/show/<filename>')
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('index.html', filename=filename)


@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
